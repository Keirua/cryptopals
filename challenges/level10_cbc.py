from cryptolib import *
from base64 import b64decode
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

if __name__ == '__main__':
	block_size = 16
	iv = b'\x00' * block_size
	key =       b"YELLOW SUBMARINE"
	plaintext = b"Salut tout le monde !"
	plaintext_padded = iv + pkcs(plaintext, 16)
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