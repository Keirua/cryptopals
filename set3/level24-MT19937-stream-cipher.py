from level21_mt19937 import mt32
from random import randint
def mt19937_streamcipher(text, seed):
	out = bytes()
	m = mt32(seed)

	for offset in range(len(text)):
		keystream = (m.extract_number() % 256)
		out += bytes([text[offset] ^ keystream])

	return out

plaintext = b"The history of the Internet begins with the development of electronic computers in the 1950s. Initial concepts of wide area networking originated in several computer science laboratories in the United States, United Kingdom, and France.[1] The US Department of Defense awarded contracts as early as the 1960s, including for the development of the ARPANET project, directed by Robert Taylor and managed by Lawrence Roberts. The first message was sent over the ARPANET in 1969 from computer science Professor Leonard Kleinrock's laboratory at University of California, Los Angeles (UCLA) to the second network node at Stanford Research Institute (SRI)."

seed = randint(0, 1<<16)
ciphertext = mt19937_streamcipher(plaintext, seed)
plaintext2 = mt19937_streamcipher(ciphertext, seed)
print(plaintext2)
print("Seed =", seed)

control_text = b'A' * 14
control_cipher = mt19937_streamcipher(control_text, seed)

# Attempt to break and find the key using bruteforce
for i in range(0, 1<<16):
	attempt = mt19937_streamcipher(control_text, i)
	if attempt == control_cipher:
		print("the broken key is", i)
		break;