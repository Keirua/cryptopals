from binascii import unhexlify,hexlify
import string

cipher = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def single_byte_xor_decrypt(cipher, key):
	out = []
	for i in range(len(cipher)):
		unxor = chr(cipher[i] ^ key)
		if unxor.lower() in string.ascii_lowercase:
			out.append(unxor.lower())
	return ''.join(out)

def count_letters(unciphered):
	nb = 0
	for c in unciphered:
		if c in string.ascii_letters:
			nb += 1
	return nb

# takes a string and returns a dict of the frequency of each char
def compute_frequency(text):
	freqs = {}
	for c in text:
		c = c.lower()
		freqs[c] = 1 if c not in freqs else freqs[c] +1
	for k in freqs:
		freqs[k] /= len(text)
	return freqs

def compute_chi2_score(freqs, text_len):
	if len(freqs) < 5:
		return 1000000000000
	en_freqs = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}
	chi = 0.0
	for l in string.ascii_lowercase:
		f = 0 if l not in freqs else freqs[l]
		sqrt_numerator = (f - 0.01*en_freqs[l])*text_len
		chi += (sqrt_numerator * sqrt_numerator) / (en_freqs[l] * 0.01* text_len)
	return chi

unxors = []
for i in range(256):
	unxored = single_byte_xor_decrypt(unhexlify(cipher), i)
	freqs = compute_frequency(unxored)
	chi2_score = compute_chi2_score(freqs, len(cipher))
	unxors.append({
		'unciphered': unxored,	
		'chi2_score': chi2_score,
		'key': i
	})

sorted_chi = sorted(unxors, key=lambda k: k['chi2_score'])
for v in sorted_chi[0:10]:
	print(v['key'], v['chi2_score'], v['unciphered'])

# unxored_88 = single_byte_xor_decrypt(unhexlify(cipher), 88)
# freq_88 = compute_frequency(unxored_88)
# letter_order = letters_by_frequency(freq_88)
# print(i)
# print(freq_88)
# print(letter_order)