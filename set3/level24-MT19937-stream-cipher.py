from level21_mt19937 import mt32
from random import randint
from base64 import b64encode
from time import time
from binascii import hexlify, unhexlify

def mt19937_streamcipher(text, seed):
	out = bytes()
	m = mt32(seed)

	for offset in range(len(text)):
		keystream = (m.extract_number() % 256)
		out += bytes([text[offset] ^ keystream])

	return out

# Part1: encrypt and find the seed used to encrypt

plaintext = b"The history of the Internet begins with the development of electronic computers in the 1950s. Initial concepts of wide area networking originated in several computer science laboratories in the United States, United Kingdom, and France.[1] The US Department of Defense awarded contracts as early as the 1960s, including for the development of the ARPANET project, directed by Robert Taylor and managed by Lawrence Roberts. The first message was sent over the ARPANET in 1969 from computer science Professor Leonard Kleinrock's laboratory at University of California, Los Angeles (UCLA) to the second network node at Stanford Research Institute (SRI)."

seed = randint(0, 1<<16)
ciphertext = mt19937_streamcipher(plaintext, seed)
plaintext2 = mt19937_streamcipher(ciphertext, seed)
print(plaintext2)
print("Seed =", seed)

def break_key():
	control_text = b'A' * 14
	control_cipher = mt19937_streamcipher(control_text, seed)

	# Attempt to break and find the key using bruteforce
	for i in range(0, 1<<16):
		attempt = mt19937_streamcipher(control_text, i)
		if attempt == control_cipher:
			print("the broken key is", i)
			break;

## Part 2: generate and break a token

# generate a 16 byte token
def generate_token(seed):
	m = mt32(seed)
	return hexlify(bytes([m.extract_number() % 256 for i in range(16)]))
	
# Let's assume we want to see if the token was generated in the last 24 hours
def break_token_seed():
	for i in range(int(time())-86400, int(time())):
		token = generate_token(i)
		if(token == target_token):
			print("Seed is", seed)
			return
	raise ValueError("The token was not generated in the last 24 hours")


seed = int(time() - 80000)
target_token = generate_token(seed)
print(seed, target_token)
break_token_seed()
