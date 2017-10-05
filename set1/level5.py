from binascii import hexlify

plaintext = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
expected = b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

def xorrepeatkey(plaintext, key):
	xored = []
	for i in range(len(plaintext)):
		xored.append(plaintext[i] ^ key[i%len(key)])
	return bytes(xored)

ciphertext = hexlify(xorrepeatkey(plaintext, b"ICE"))

print (plaintext)
print (ciphertext)
print (ciphertext == expected)