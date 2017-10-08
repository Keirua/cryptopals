from binascii import unhexlify,hexlify

fd = open("../cryptopals/data/8.txt", "r")
ciphers = [x for x in fd.read().split("\n")]

# print(ciphers[0])
# print(unhexlify(ciphers[0]))

hex0 = unhexlify(ciphers[0])

def compute_block_occurences(cipher, block_size=16):
	occurences = {}
	index = 0
	while index + block_size <= len(cipher):
		block = cipher[index:index+16]
		occurences[block] = 1 if block not in occurences else occurences[block] +1
		index += block_size
	return occurences

# occurence0 = compute_block_occurences(hex0)
occurences = []
for c in ciphers:
	occurence = compute_block_occurences(unhexlify(c))
	occurences.append({
		'ciphertext': c,
		'occurences': occurence
	})

occurences = sorted(occurences, key = lambda k: len(k['occurences'].keys()))

print("occ")
for o in occurences[0:3]:
	print (
		len(o['occurences'].keys()),
		o['ciphertext'],
	)

# From this we can see that one of the ciphertexts does not have a random distribution:
# some 16bytes block repeat themselves