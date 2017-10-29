from base64 import b64decode
from Crypto.Cipher import AES

fd = open("7.txt", "r")
ciphertext = b64decode(fd.read())

# Key is 16 bytes long, which is the key length for AES-128
key=b"YELLOW SUBMARINE"
aes_ecb128 = AES.new(key, AES.MODE_ECB)
plaintext = aes_ecb128.decrypt(ciphertext)

print(plaintext)