from random import randint
from binascii import hexlify, unhexlify
from level10_cbc import aes_128_ecb_encrypt, aes_128_cbc_encrypt, pkcs
# could not import due to python import system
# from "../set1/level8.py" import count_block_occurences 
fd = open("text.txt", 'r')
plaintext = fd.read().encode('ascii')

# taken from level8
def count_block_occurences(cipher, block_size=16):
	occurences = {}
	index = 0
	while index + block_size <= len(cipher):
		block = cipher[index:index+16]
		occurences[block] = 1 if block not in occurences else occurences[block] +1
		index += block_size
	return occurences

def n_random_bytes(n=16):
	return bytes([randint(0,255) for i in range(n)])

def oracle_encode(plaintext):
	r = randint(0,1)
	key = n_random_bytes()
	
	before = bytearray(n_random_bytes(randint(5,10)))
	after = bytearray(n_random_bytes(randint(5,10)))
	# Repeat the plaintext 5 times in order to make sure publicated blocks appear
	padded_plaintext = pkcs(bytes(before + bytearray(plaintext*5) + after), 16, b'\x00')

	if r == 0:
		ciphertext = aes_128_ecb_encrypt(padded_plaintext, key)
		mode = 'ecb'
	else:
		ciphertext = aes_128_cbc_encrypt(padded_plaintext, key, n_random_bytes())
		mode = 'cbc'
	return {
		'ciphertext': ciphertext,
		'mode': mode
	}

def detect_mode(oracle):
	block_counts = count_block_occurences(encoded['ciphertext'])
	mode = 'cbc' if len(block_counts.keys()) == len(encoded['ciphertext']) / 16 else 'ecb'
	print(encoded['mode'] == mode)

for i in range(10):
	encoded = oracle_encode(plaintext)
	detect_mode(encoded)

	
