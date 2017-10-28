from level21_mt19937 import mt32

def mt19937_streamcipher(text, seed):
	out = bytes()
	m = mt32(seed)

	for offset in range(len(text)):
		keystream = (m.extract_number() % 256)
		out += bytes([text[offset] ^ keystream])

	return out

plaintext = b"The history of the Internet begins with the development of electronic computers in the 1950s. Initial concepts of wide area networking originated in several computer science laboratories in the United States, United Kingdom, and France.[1] The US Department of Defense awarded contracts as early as the 1960s, including for the development of the ARPANET project, directed by Robert Taylor and managed by Lawrence Roberts. The first message was sent over the ARPANET in 1969 from computer science Professor Leonard Kleinrock's laboratory at University of California, Los Angeles (UCLA) to the second network node at Stanford Research Institute (SRI)."

ciphertext = mt19937_streamcipher(plaintext, 123)
plaintext2 = mt19937_streamcipher(ciphertext, 123)
print(plaintext2)