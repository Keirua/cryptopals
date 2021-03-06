from cryptolib import *
from base64 import b64decode
import string

# Not the best python code I've written...
def edit_ctr(ciphertext, nonce, key, index, newtext):
    # Locate the block, offset we want to edit
    index_in_block = index % 16
    counter = index // 16
    offset = counter * 16
    current_block = ciphertext[offset:offset+16]
    # decrypt
    aesctr = aes_128_ecb_encrypt(create_input(nonce, counter), key)
    plaintext_for_this_block = list(xor_combine(aesctr, current_block))
    # edit
    plaintext_for_this_block[index_in_block] = ord(newtext)
    # reencrypt
    local_edited_ciphertext = xor_combine(aesctr, bytes(plaintext_for_this_block))

    edited_ciphertext = list(ciphertext)

    edited_ciphertext[offset:offset+16] = list(local_edited_ciphertext)
    return bytes(edited_ciphertext)

# Let's assume we have an API for edition that allow us
# to edit one byte of the ciphertext
random_key = n_random_bytes(16)
nonce = 0

def edit_api(ciphertext, index, newtext):
    return edit_ctr(ciphertext, nonce, random_key, index, newtext)

fd = open("../cryptopals/data/25.txt", 'r')
lv7ciphertext = b64decode(fd.read().strip('\n').encode('ascii'))
lv7plaintext = aes_128_ecb_decrypt(lv7ciphertext, b"YELLOW SUBMARINE")

ciphertext = aes_128_ctr(lv7plaintext, random_key, nonce)
# Some tests to see that our edit API works as expected
ciphertext = edit_api(ciphertext, 0, b'A')
ciphertext = edit_api(ciphertext, 1, b'B')
ciphertext = edit_api(ciphertext, 5, b'O')
ciphertext = edit_api(ciphertext, 62, b'8')

plaintext_after_edit = aes_128_ctr(ciphertext, random_key, 0)
print("edited plaintext", plaintext_after_edit[:120])

# Let's reset and break it
ciphertext = aes_128_ctr(lv7plaintext, random_key, nonce)
# Editing the ciphertext gives us plenty of information to decipher the ciphertext
broken_plaintext = bytes()
for i in range(len(ciphertext)):
    for v in string.printable:
        edited_ciphertext = edit_api(ciphertext, i, v.encode('ascii'))
        if (ciphertext[i] == edited_ciphertext[i]):
            broken_plaintext += v.encode('ascii')
            continue

print(broken_plaintext)









