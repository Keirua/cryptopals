from binascii import unhexlify,hexlify
import string

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

if __name__ == '__main__':
	cipher = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	print(single_byte_xor_decrypt_best_key(unhexlify(cipher)))