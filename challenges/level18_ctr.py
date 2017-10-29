from cryptolib import aes_128_ctr
from base64 import b64decode

ciphertext = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
key = b"YELLOW SUBMARINE"
nonce = 0

hex_cipher = b64decode(ciphertext)
print(aes_128_ctr(hex_cipher, key, 0))
#aesctr0 = aes_128_ecb_encrypt(create_input(nonce, 0), key)
#print(xor_combine(aesctr0, hex_cipher[0:16]))

# aesctr1 = aes_128_ecb_encrypt(bytes([0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0]), key)
# print(xor_combine(aesctr1, hex_cipher[16:32]))
# aesctr2 = aes_128_ecb_encrypt(create_input(nonce, 2), key)
# print(xor_combine(aesctr2, hex_cipher[2:18]))


