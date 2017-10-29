from binascii import unhexlify,hexlify
from base64 import b64decode
from level18_ctr import aes_128_ctr
from random import randint

en_rank = {
    'e': 27,
    't': 26,
    'a': 25,
    'o': 24,
    'i': 23,
    'n': 22,
    's': 21,
    'r': 20,
    'h': 19,
    'l': 18,
    'd': 17,
    'c': 16,
    'u': 15,
    'm': 14,
    'f': 13,
    'p': 12,
    'g': 11,
    'w': 10,
    'y': 9,
    'b': 8,
    'v': 7,
    'k': 6,
    'x': 5,
    ' ': 4,
    'j': 3,
    'q': 2,
    'z': 1
}

def xorrepeatkey(plaintext, key):
	xored = [plaintext[i] ^ key[i%len(key)] for i in range(len(plaintext))]
	return bytes(xored)

def single_byte_xor_decrypt(cipher, key):
	out = [chr(c ^ key) for c in cipher]
	return ''.join(out)

def compute_score(text):
	score = 0
	for c in text:
		c = c.lower()
		score += 0 if c not in en_rank else en_rank[c]
	return score

def single_byte_xor_decrypt_best_key(cipher):
	unxors = []
	for i in range(256):
		unxored = single_byte_xor_decrypt(cipher, i)
		unxors.append({
			'cipher': cipher,
			'unciphered': unxored,
			'score': compute_score(unxored),
			'key': i
		})
	# sorted_unxors = sorted(unxors, key=lambda k: k['score'])
	return max(unxors, key=lambda k: k['score'])

def generate_block(ciphertext, key_length, offset):
	block = bytearray()
	index = 0
	while (index + offset) < len(ciphertext):
		block.append(ciphertext[index+offset])
		index += key_length
	return bytes(block)

def break_repeating_key_xor_with_length(ciphertext, key_length):
	key = bytearray()
	for offset in range(key_length):
		block = generate_block(ciphertext, key_length, offset)
		best_match = single_byte_xor_decrypt_best_key(block)
		key.append(best_match['key'])
	return key

def n_random_bytes(n=16):
    return bytes([randint(0,255) for i in range(n)])


# Level 20 code
fd = open("../cryptopals/data/20.txt", "r")
plaintexts = [b64decode(line) for line in fd.read().split("\n") if line.strip() != '' ]

key = n_random_bytes(16)
nonce = 0

ciphers = [aes_128_ctr(plaintext, key, nonce) for plaintext in plaintexts]
shortest_cipher = min(ciphers, key=lambda k: len(k))
compound_ciphers = b''.join([ c[:len(shortest_cipher)] for c in ciphers ])

print(len(shortest_cipher), shortest_cipher)
#print(compound_ciphers)

length = len(shortest_cipher)
key = break_repeating_key_xor_with_length(compound_ciphers, length)
print("key: '{}' ({})".format(str(key), len(key)))
print(xorrepeatkey(compound_ciphers, key))
