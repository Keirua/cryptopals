from base64 import b64decode
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify



def pkcs(s:str, block_size: int, padding: bytes) -> str:
	remainder = len(s) % block_size
	if remainder == 0:
		return s
	return s + padding * (block_size-remainder)

def aes_128_ecb_decrypt(ciphertext, key):
	aes_ecb128 = AES.new(key, AES.MODE_ECB)
	return aes_ecb128.decrypt(ciphertext)

def aes_128_ecb_encrypt(plaintext, key):
	aes_ecb128 = AES.new(key, AES.MODE_ECB)
	return aes_ecb128.encrypt(plaintext)

def aes_128_cbc_decrypt(ciphertext, iv, key):
	aes_cbc128 = AES.new(key, AES.MODE_CBC, iv)
	return aes_cbc128.decrypt(ciphertext)

def aes_128_cbc_encrypt(plaintext, iv, key):
	aes_cbc128 = AES.new(key, AES.MODE_CBC, iv)
	return aes_cbc128.encrypt(plaintext)


def xor_combine(hex_a1, hex_a2):
	return bytes([x1 ^ x2 for (x1, x2) in zip(hex_a1, hex_a2)])

def cbc_encrypt(plaintext_padded, iv, key):
	previous_cipher = iv
	out = bytearray()
	idx = 0
	while(idx+block_size <= len(plaintext_padded)):
		current_plaintext = plaintext_padded[idx:idx+block_size]
		xored = xor_combine(current_plaintext, previous_cipher)
		previous_cipher = aes_128_ecb_encrypt(xored, key)
		out += previous_cipher
		idx += block_size
	return bytes(out)

def cbc_decrypt(cipher_padded, iv, key):
	previous_cipher = iv
	out = bytearray()
	idx = 0
	while(idx + block_size <= len(cipher_padded)):
		curr_block = cipher_padded[idx:idx+block_size]
		uncipher = aes_128_ecb_decrypt(curr_block, key)
		xored = xor_combine(uncipher, previous_cipher)
		out += xored
		previous_cipher = curr_block
		idx += block_size
	return out


if __name__ == '__main__':
	block_size = 16
	iv = b'\x00' * block_size
	key =       b"YELLOW SUBMARINE"
	plaintext = b"Salut tout le monde !"
	plaintext_padded = iv + pkcs(plaintext, 16, b'\x00')
	print(aes_128_ecb_decrypt(aes_128_ecb_encrypt(plaintext_padded, key), key))

	fd = open("../cryptopals/data/10.txt", "r")
	ciphertext = (b64decode("".join(fd.read())))

	print(ciphertext)
	print(len(ciphertext), len(ciphertext)%16)
	print(cbc_decrypt(ciphertext, iv, key))









# Debugging
# key =       b"YELLOW SUBMARINE"
# plaintext = b"Salut tout le monde !"
# iv = b'\x00' * 16
# 
# print(" == OpenSSL's solution ==")
# print(" With CBC")
# aes_encrypted = aes_128_cbc_encrypt(pkcs(plaintext, 16, b'\x00'), iv, key)
# print("aes_encrypted")
# print(aes_encrypted)
# print("aes_decrypted")
# print(aes_128_cbc_decrypt(aes_encrypted, iv, key))
# 
# print(" With ECB")
# aes_encrypted = aes_128_ecb_encrypt(pkcs(plaintext, 16, b'\x00'), key)
# print("aes_encrypted")
# print(aes_encrypted)
# print("aes_decrypted")
# print(aes_128_ecb_decrypt(aes_encrypted, key))
# 
# aes_encrypted = cbc_encrypt(pkcs(plaintext, 16, b'\x00'), iv, key)
# print(" == My solution ==")
# print("aes_encrypted")
# print(aes_encrypted)
# print("aes_decrypted")
# print(cbc_decrypt(aes_encrypted, iv, key))