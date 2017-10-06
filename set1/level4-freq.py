from binascii import unhexlify,hexlify
import string

# https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis

cipher = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def count_letters(unciphered):
	nb = 0
	for c in unciphered:
		if c in string.ascii_letters:
			nb += 1
	return nb

def single_byte_xor_decrypt(cipher, key):
	out = []
	for i in range(len(cipher)):
		out.append(chr(cipher[i] ^ key))
	return ''.join(out)

def compute_frequency(text):
	freqs = {}
	for l in string.ascii_lowercase:
		freqs[l] = 0 
	nb_letters = 1
	for c in text:
		c = c.lower()
		if c in string.ascii_lowercase:
			freqs[c] +1
			nb_letters += 1
	# for k in freqs:
	# 	freqs[k] /= nb_letters
	freqs['letters'] = nb_letters
	return freqs

def compute_chi2_score(freqs, text_len):
	en_freqs = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}
	chi = 0.0

	for l in string.ascii_lowercase:
		sqrt_numerator = (freqs[l] - 0.01*en_freqs[l]*text_len)
		chi += (sqrt_numerator * sqrt_numerator) / (en_freqs[l] * 0.01* text_len)
	return chi

def single_byte_xor_compute_chi2(cipher):
	unxors = []
	for i in string.ascii_letters:
		unxored = single_byte_xor_decrypt(cipher, ord(i))
		nb_letters = count_letters(unxored)
		if (nb_letters/len(unxored) < 0.5):
			continue

		freqs = compute_frequency(unxored)
		chi2_score = compute_chi2_score(freqs, freqs['letters'])
		unxors.append({
			'unciphered': unxored,	
			'chi2_score': chi2_score,
			'key': i
		})
	return unxors

fd = open("../cryptopals/data/4.txt", "r")
ciphers = [x for x in fd.read().split("\n")]

all_cipher_result = []
for c in ciphers:
	all_cipher_result += single_byte_xor_compute_chi2(unhexlify(c))

sorted_chi = sorted(all_cipher_result, key=lambda k: k['chi2_score'])
for v in sorted_chi[0:30]:
	print(v['key'], v['chi2_score'], v['unciphered'])

# unxors = []
# for i in range(256):
# 	unxored = single_byte_xor_decrypt(unhexlify(cipher), i)
# 	freqs = compute_frequency(unxored)
# 	chi2_score = compute_chi2_score(freqs, len(cipher))
# 	unxors.append({
# 		'unciphered': unxored,	
# 		'chi2_score': chi2_score,
# 		'key': i
# 	})
# 
# sorted_chi = sorted(unxors, key=lambda k: k['chi2_score'])
# for v in sorted_chi[:10]:
# 	print(v['key'], v['chi2_score'], v['unciphered'])
