from random import randint
from binascii import hexlify, unhexlify
from base64 import b64decode
from level10_cbc import aes_128_ecb_encrypt, aes_128_cbc_encrypt, pkcs
from level11_oracle import n_random_bytes
import string

before = n_random_bytes(randint(0,50))
after = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'

global_key = n_random_bytes(16)

def weird_cipher(text):
	fulltext = before
	fulltext += bytearray(text)
	fulltext += bytearray(b64decode(after))
	return aes_128_ecb_encrypt(pkcs(bytes(fulltext), 16, b'\x00'), global_key)

def break_block_length():
	# Feed block to the cipher until it has to be padded again.
	n = 1
	while len(weird_cipher(b'A' * n)) == len(weird_cipher(b'A' * (n+1))):
		n += 1
	return len(weird_cipher(b'A' * (n+1))) - len(weird_cipher(b'A' * n))

def break_ciphertext(initial_nb_As, text_offset_start):
	found = str()
	found_before = str()
	n = 1

	while(True):
		for i in range(block_length):
			crafted_block = bytes('A' * (block_length - i - 1 + initial_nb_As), 'ascii')
			cipher = weird_cipher(crafted_block)

			for c in string.printable:
				match_attempt = bytearray(crafted_block) + bytearray(found, 'ascii') + bytearray(c, 'ascii')
				if(weird_cipher(match_attempt)[text_offset_start:text_offset_start+block_length*(n)] == cipher[text_offset_start:text_offset_start+block_length*(n)]):
					found += c
					break
		# Leave as soon as we don't find new chars anymore
		if (found == found_before):
			break
		else:
			found_before = found
			n += 1
	return (bytes(found, 'ascii'))

# First, cipher with 3 times the block length. Now matter how long the prefix is,
# we'll have 2 identical block of block_length encrypted A's.
# This uses the fact that 2 identical blocks will be encrypted in the same way using ECB
block_length = break_block_length()
ciphertext = weird_cipher(b'A' * 3 * block_length)

# Now we look for 2 identical blocks of encrypted AAA...AAA's in order to see what the encrypted version look like
i = 0
similar_block = ''
while (i+2)*block_length < len(ciphertext):
	if ciphertext[i*block_length:(i+1)*block_length] == ciphertext[(i+1)*block_length:(i+2)*block_length]:
		similar_block = ciphertext[i*block_length:(i+1)*block_length]
		break;
	i +=1

# Now, we'll feed a decreasing amount of A's until the 2 encrypted block of A's disappears.
# We keep one block of A's as "buffer" so that clearly separate before and after text with our A's
for nb_offset_As in range (3*block_length, 0, -1):
	if(weird_cipher(b'A' * (nb_offset_As-1)).find(similar_block) == -1):
		break

# So, now we can craft a message with nb_offset_As * 'A' as input.
# This amount of A's will block the "before" text from the cipher to interfere (the "before" text plus our As amount to a multiple of block_length bytes),
# Now we now decrypt the unknown text like before via a timing attack, with a few more offsets than before.
text_offset_start = block_length + weird_cipher(b'A' * nb_offset_As).find(similar_block)

print (break_ciphertext(nb_offset_As, text_offset_start))
