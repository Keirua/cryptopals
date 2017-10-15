from random import randint
from binascii import hexlify, unhexlify
from base64 import b64decode
from level10_cbc import aes_128_ecb_encrypt, aes_128_cbc_encrypt, pkcs
from level11_oracle import n_random_bytes
import string

unknown = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
plaintext = b"The history of the Internet begins with the development of electronic computers in the 1950s."

global_key = n_random_bytes(16)

def weird_cipher(text):
	fulltext = bytearray(text)
	#fulltext += bytearray(b64decode(unknown))
	fulltext += bytearray(plaintext)
	return aes_128_ecb_encrypt(pkcs(bytes(fulltext), 16, b'\x00'), global_key)

cipher = weird_cipher(plaintext)

def break_block_length():
	# Feed block to the cipher until it has to be padded again.
	n = 1
	while len(weird_cipher(b'A' * n)) == len(weird_cipher(b'A' * (n+1))):
		n += 1
	return len(weird_cipher(b'A' * (n+1))) - len(weird_cipher(b'A' * n))



block_length = break_block_length()
print(block_length)

def break_ciphertext():
	found = str()
	
	for i in range(block_length-1):
		crafted_block = bytes('A' * (block_length - len(found) - 1), 'ascii')
		cipher = weird_cipher(crafted_block)

		for c in string.printable:
			match_attempt = bytearray(crafted_block) + bytearray(found, 'ascii') + bytearray(c, 'ascii')
			#print(match_attempt)
			#print(" > ", c)
			#print(weird_cipher(match_attempt)[:block_length])
			#print(cipher[:block_length])
			if(weird_cipher(match_attempt)[:block_length] == cipher[:block_length]):
				found += c
				# print("\n" * 3)
				break
	print(found)
break_ciphertext()

# print(hexlify(weird_cipher(b'\x41' * 15)))
# attempt = bytearray(b'\x41'*15) + bytes('T', 'ascii')
# print(hexlify(aes_128_ecb_encrypt(bytes(attempt), global_key)))