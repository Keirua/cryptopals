from cryptolib import *
from base64 import b64decode


def aes_128_ctr(text, key, nonce):
    out = bytes()
    offset = 0
    counter = 0
    while offset < len(text):
        current_plaintext = text[offset:offset+16]
        aesctr = aes_128_ecb_encrypt(create_input(nonce, counter), key)
        cipher = xor_combine(aesctr, current_plaintext)
        out += cipher
        counter += 1
        offset += 16
    return out

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



fd = open("../cryptopals/data/25.txt", 'r')
lv7ciphertext = b64decode(fd.read().strip('\n').encode('ascii'))
lv7plaintext = aes_128_ecb_decrypt(lv7ciphertext, b"YELLOW SUBMARINE")

random_key = n_random_bytes(16)
# print(lv7plaintext)

ciphertext = aes_128_ctr(lv7plaintext, random_key, 0)
# I'm bOck
ciphertext = edit_ctr(ciphertext, 0, random_key, 5, b'O')
ciphertext = edit_ctr(ciphertext, 0, random_key, 62, b'8')
#
plaintext_after_edit = aes_128_ctr(ciphertext, random_key, 0)
print("edited plaintext", plaintext_after_edit[:120])

