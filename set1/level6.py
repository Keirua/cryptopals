from binascii import hexlify
from base64 import b64decode
from level3_freq import single_byte_xor_decrypt_best_key
from level5 import xorrepeatkey

def different_bits(a, b):
	return sum((a & (1 << i)) != (b & (1 << i)) for i in range(0, 8))

def hamming(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(different_bits(el1, el2) for el1, el2 in zip(s1, s2))


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

# Some "unit tests"
# print(generate_block(b"abcdefgh", 2, 0) == b"aceg")
# print(generate_block(b"abcdefgh", 2, 1) == b"bdfh")
# print(generate_block(b"abcdefg", 2, 1) == b"bdf")
# print(generate_block(b"abcdefgh", 10, 1) == b"b")
a = b"this is a test"
b = b"wokka wokka!!!"
print(hamming(a, b) == 37)

fd = open("../cryptopals/data/6.txt", "r")
cipher = b64decode("".join(fd.read().split("\n")))

def generate_distances(text, nb_block_for_avg_distance=4):
	distances = []
	for key_size in range (2, 40):
		avg_distance = 0
		for i in range(nb_block_for_avg_distance):
			b1 = (text[0:key_size])
			b2 = (text[(i+1)*key_size:(i+2)*key_size])		
			avg_distance += hamming(b1,b2)
		avg_distance /= (nb_block_for_avg_distance * key_size)
		distances.append({
			'key_length':key_size,
			'difference':avg_distance
		})
	return distances

distances = generate_distances(cipher)
sorted_distances = (sorted(distances, key = lambda k: k['difference']))

# When trying a couple probable distances, we find that 5 and 29 come very often
for good_matches in sorted_distances[0:2]:
	print(good_matches)
	length = good_matches['key_length']
	key=break_repeating_key_xor_with_length(cipher, length)
	print("key: '{}' ({})".format(str(key), len(key)))
	print(xorrepeatkey(cipher, key))
