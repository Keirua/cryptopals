from binascii import unhexlify,hexlify
import string
from level3_freq import single_byte_xor_decrypt_best_key

fd = open("../cryptopals/data/4.txt", "r")
ciphers = [x for x in fd.read().split("\n")]

best_cipher_results = []
for c in ciphers:
	best_cipher_results.append(single_byte_xor_decrypt_best_key(unhexlify(c)))

print(max(best_cipher_results, key=lambda k: k['score']))


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
