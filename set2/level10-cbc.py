from base64 import b64decode
from Crypto.Cipher import AES

fd = open("../cryptopals/data/10.txt", "r")
ciphertext = b64decode(fd.read())

block_size = 16

iv = b'\x00' * block_size

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

key =       b"YELLOW SUBMARINE"
plaintext = b"Salut tout le monde !"

plaintext_padded = iv + pkcs(plaintext, 16, b'\x00')

print(aes_128_ecb_decrypt(aes_128_ecb_encrypt(plaintext_padded, key), key))
