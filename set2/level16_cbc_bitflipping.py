from random import randint
from binascii import hexlify, unhexlify
from base64 import b64decode
from level10_cbc import aes_128_cbc_encrypt,aes_128_cbc_decrypt, pkcs
from level11_oracle import n_random_bytes
import string
import pprint
global_key = n_random_bytes(16)

def parse_params(parameters):
	d = {}
	kvList = parameters.split(b';')
	for kv in kvList:
		if b'=' not in kv:
			continue
		kvA = kv.split(b'=')
		if(len(kvA) != 0):
			d[kvA[0]] = kvA[1]
	return d

def custom_cipher(plaintext):
	if b'=' in plaintext or b';' in plaintext:
		raise ValueError('= and ; are forbidden')
	fulltext = b'comment1=cooking%20MCs;userdata='
	fulltext += bytearray(plaintext)
	fulltext += bytearray(b';comment2=%20like%20a%20pound%20of%20bacon')

	return aes_128_cbc_encrypt(pkcs(bytes(fulltext), 16, b'\x00'), b'\x00' * 16, global_key)

def draw_blocks_and_check(ciphertext):
	plaintext = aes_128_cbc_decrypt(ciphertext, b'\x00' * 16, global_key)
	for i in range(0, len(plaintext), 16):
		print(plaintext[i:i+16])
	params = parse_params(plaintext)
	#pp = pprint.PrettyPrinter(indent=4)
	pprint.pprint(params)
	print("Are we admin ?", b'admin' in params)

# We provide a plaintext with only valid characters
payload = b"\x3Aadmin\x3Ctrue"
ciphertext = custom_cipher(payload)

print("\tBefore modification")
draw_blocks_and_check(ciphertext)

print()

# We need to find a proper way to hack this
for i in range(0, 5+1): # we can only use 
	# then we modify the corresponding bit in the previoud so that it can be decoded
	ciphertext_hacked = bytearray(custom_cipher(b'a' * i + payload))
	# The offset 0 and 6 are the position of the ; and = in the previous block
	if(ciphertext_hacked[16+0+i] & 1 == 0 and ciphertext_hacked[16+6+i] & 1 == 1):
		print("hack possible !")
		ciphertext_hacked[16+0+i] |= 1 # we want to set the first bit to 1 in order to have 0x3B = ';''
		ciphertext_hacked[16+6+i] &= ~1 # we want to set the first bit to 0 in order to have 0x3D = '='
		break;
	else:
		print("hack impossible... try again with another offset")

print("\tAfter modification")
draw_blocks_and_check(bytes(ciphertext_hacked))

print(b';'.hex()) # = b';' = 0x3b = 111011
print(b'\x3A')    # = 0x3A = b111010 = b':'

print(b'='.hex()) # = b'=' = 0x3D = b111101
print(b'\x3C')    # = 0x3C = b111100 = b'<'