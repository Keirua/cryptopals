from binascii import unhexlify,hexlify

cipher = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def single_byte_xor_decrypt(cipher, key):
	out = []
	for i in range(len(cipher)):
		out.append(chr(cipher[i] ^ key))
	return ''.join(out)

for i in range(256):
	print(hexlify(single_byte_xor_decrypt(unhexlify(cipher), i)))