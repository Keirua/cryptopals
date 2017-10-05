from binascii import unhexlify,hexlify
import string

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

def count_letters(unciphered):
	nb = 0
	for c in unciphered:
		if c in string.ascii_letters:
			nb += 1
	return nb

def single_byte_xor_decrypt_bruteforce(hex_cipher):
	unxors = []
	for i in range (256):
		unciphered = single_byte_xor_decrypt(hex_cipher, i)
		# discards ciphers where there is a low amount of characters
		nb_letters = count_letters(unciphered)
		if (nb_letters/len(unciphered) < 0.5):
			continue
		# if there are more than 50% letters, try to count words
		founds = find_words(unciphered, common_words)
		if len(founds) > 1:
			unxors.append({
				'unciphered': unciphered,	
				'hex_cipher': hex_cipher,
				'nb_found_words': len(founds),
				'key': i
			})
	return unxors

fd = open("4.txt", "r")
ciphers = [x for x in fd.read().split("\n")]

all_cipher_result = []
for c in ciphers:
	all_cipher_result += single_byte_xor_decrypt_bruteforce(unhexlify(c))

sorted_results = sorted(all_cipher_result, key=lambda k: k['nb_found_words'])

for v in sorted_results[-10:]:
	print(v['key'], v['unciphered'], v['nb_found_words'], hexlify(v['hex_cipher']))

# time python level4.py
# 21 nOWTHATTHEPARTYISJUMPING* 13 b'7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f'
# 53 Now that the party is jumping
# 13 b'7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f'
# python level4.py  41,59s user 0,01s system 99% cpu 41,606 total