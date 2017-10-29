from cryptolib import aes_128_cbc_encrypt, aes_128_cbc_decrypt, n_random_bytes, pkcs, xor_combine
from binascii import hexlify

# Don't ever use the key as IV with CBC mode.
# An attacker that can modify ciphertext in flight
# can get the receiver to decrypt a value that will reveal the key. 

def aes_128_cbc_encrypt_with_key(ciphertext, key):
	return aes_128_cbc_encrypt(ciphertext, key, key)

def aes_128_cbc_decrypt_with_key(ciphertext, key):
	return aes_128_cbc_decrypt(ciphertext, key, key)

key = n_random_bytes(16)
print("key is", hexlify(key))

# Use your code to encrypt a message that is at least 3 blocks long: 
cipher123 = aes_128_cbc_encrypt_with_key(b'A' * 3 * 16, key)

# Modify the message (you are now the attacker): 
cipher101 = bytes(cipher123[0:16] + b'\x00' * 16 + cipher123[0:16])

# Decrypt the message (you are now the receiver) and raise the appropriate error if high-ASCII is found.
plain101 = aes_128_cbc_decrypt_with_key(cipher101, key)

broken_key = xor_combine(plain101[0:16], plain101[32:48])
print("The broken key is", hexlify(broken_key))
print("Does it matches the original key ?", broken_key == key)