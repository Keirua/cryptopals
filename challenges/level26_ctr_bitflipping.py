from level16_cbc_bitflipping import parse_params, draw_blocks_and_check
from cryptolib import aes_128_ctr, n_random_bytes
import string
import pprint
import random

global_key = n_random_bytes(16)

def custom_cipher(plaintext):
	#if b'=' in plaintext or b';' in plaintext:
	#	raise ValueError('= and ; are forbidden')
	fulltext = b'comment1=cooking%20MCs;userdata='
	fulltext += bytearray(plaintext)
	fulltext += bytearray(b';comment2=%20like%20a%20pound%20of%20bacon')

	return aes_128_ctr(bytes(fulltext), global_key, 0)



print("Before")
payload = b"a\x3Aadmin\x3Ctrue"
ciphertext = custom_cipher(bytes(payload))
draw_blocks_and_check(aes_128_ctr(ciphertext, global_key, 0))

print()
print("After")

def is_admin(ciphertext_hacked):
	return b'admin' in parse_params(aes_128_ctr(bytes(ciphertext_hacked), global_key, 0))

l = 1
while True:
	padding = b'a' * l
	print("trying with {} a's -> {}".format(l, padding))
	payload = bytearray(b"\x3Aadmin\x3Ctrue")
	ciphertext = custom_cipher(bytes(padding + payload))
	ciphertext_hacked = bytearray(custom_cipher(bytes(padding+payload)))

	# The offset 0 and 6 are the position of the ; and = in the previous block
	ciphertext_hacked[32 + len(padding) + 0] |= 1 # we want to set the first bit to 1 in order to have 0x3B = ';''
	ciphertext_hacked[32 + len(padding) + 6] &= ~1 # we want to set the first bit to 0 in order to have 0x3D = '='		break;

	if(is_admin(bytes(ciphertext_hacked))):
		break
	
	l += 1


draw_blocks_and_check(aes_128_ctr(ciphertext_hacked, global_key, 0))