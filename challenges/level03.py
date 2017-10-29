from binascii import unhexlify,hexlify

cipher = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def single_byte_xor_decrypt(cipher, key):
	out = []
	for i in range(len(cipher)):
		out.append(chr(cipher[i] ^ key))
	return ''.join(out)

def load_word_list(filename):
	fd = open(filename, "r")
	return [x for x in fd.read().split("\n") if len(x) >= 3]

def find_words(unciphered, word_list):
	founds = []
	for w in word_list:
		if unciphered.lower().find(w) != -1:
			founds.append(w)
	return founds

common_words = load_word_list("google-10000-english.txt")
hex_cipher = unhexlify(cipher)

def single_byte_xor_decrypt_bruteforce(hex_cipher):
	unxors = []
	for i in range (256):
		unciphered = single_byte_xor_decrypt(hex_cipher, i)
		founds = find_words(unciphered, common_words)
		unxors.append({
			'unciphered': unciphered,	
			'hex_cipher': hex_cipher,
			'found_words': founds,
			'key': i
		})
	return unxors

unxors = single_byte_xor_decrypt_bruteforce(hex_cipher)
sorted_unxors = sorted(unxors, key=lambda k: len(k['found_words']))

for v in sorted_unxors[-10:]:
	print(v['key'], len(v['found_words']), v['unciphered'], v['found_words'])