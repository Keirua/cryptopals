from base64 import b64decode
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

ciphertext = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
key = b"YELLOW SUBMARINE"
nonce = 0

def create_input (nonce, counter):
	return bytes([
		(nonce & 0x00000000000000FF),
		(nonce & 0x000000000000FF00) >> 8,
		(nonce & 0x0000000000FF0000) >> 16,
		(nonce & 0x00000000FF000000) >> 24,
		(nonce & 0x000000FF00000000) >> 32,
		(nonce & 0x0000FF0000000000) >> 40,
		(nonce & 0x00FF000000000000) >> 48,
		(nonce & 0xFF00000000000000) >> 56,
		(counter & 0x00000000000000FF),
		(counter & 0x000000000000FF00) >> 8,
		(counter & 0x0000000000FF0000) >> 16,
		(counter & 0x00000000FF000000) >> 24,
		(counter & 0x000000FF00000000) >> 32,
		(counter & 0x0000FF0000000000) >> 40,
		(counter & 0x00FF000000000000) >> 48,
		(counter & 0xFF00000000000000) >> 56,
	])

def aes_128_ecb_encrypt(plaintext, key):
	aes_ecb128 = AES.new(key, AES.MODE_ECB)
	return aes_ecb128.encrypt(plaintext)

def xor_combine(hex_a1, hex_a2):
	return bytes([x1 ^ x2 for (x1, x2) in zip(hex_a1, hex_a2)])

def aes_128_ctr(text, key, nonce):
	out = bytes()
	offset = 0
	counter = 0
	while offset < len(text):
		current_plaintext = text[offset:offset+16]
		aesctr = aes_128_ecb_encrypt(create_input(nonce, counter), key)
		cipher = xor_combine(aesctr, current_plaintext)
		out += cipher
		counter += 1
		offset += 16
	return out


hex_cipher = b64decode(ciphertext)
print(aes_128_ctr(hex_cipher, key, 0))
#aesctr0 = aes_128_ecb_encrypt(create_input(nonce, 0), key)
#print(xor_combine(aesctr0, hex_cipher[0:16]))

# aesctr1 = aes_128_ecb_encrypt(bytes([0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0]), key)
# print(xor_combine(aesctr1, hex_cipher[16:32]))
# aesctr2 = aes_128_ecb_encrypt(create_input(nonce, 2), key)
# print(xor_combine(aesctr2, hex_cipher[2:18]))


