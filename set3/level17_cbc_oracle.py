from base64 import b64decode
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
from random import randint

# Implementation of PKCS7
# https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7
def pkcs(s:str, block_size: int) -> str:
    remainder = len(s) % block_size
    return s + bytes([block_size-remainder for i in range(block_size-remainder)])

def pkcs_strip(s):
    if(len(s) <= 0):
        return s
    last_value = s[len(s)-1]

    if(last_value not in range(1,16+1)):
        raise ValueError("Not a pkcs-padded string : {}".format(s))

    for i in range(1, last_value+1):
        if s[-i] != last_value:
            raise ValueError("Not a pkcs-padded string : {}".format(s))
    return s[:len(s)-last_value]

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
    block_size = 16
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
    block_size = 16
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

def n_random_bytes(n=16):
    return bytes([randint(0,255) for i in range(n)])

# Level16 code
strs = [
    b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]

def generate_token(key):
    index = randint(0, len(strs)-1)
    random_str = b64decode(strs[index])
    iv = bytes([ 0 ] * 16)

    ciphertext = cbc_encrypt(pkcs(random_str, 16), iv, key)
    return ciphertext, iv


def consume_token(ciphertext, iv):
    plaintext = cbc_decrypt(ciphertext, iv, global_key)
    try:
        pkcs_strip(plaintext)
      
    except ValueError:
        return False
    return True

# The breaking code
def craft_previous(byte_value, suffix):
    return bytes(b'A' * (15 - len(suffix)) + byte_value + suffix)

def craft_suffix(previous_block, known, offset):
    l = [previous_block[15-i] ^ ord(known[len(known)-1-i]) ^ (offset+1) for i in range(offset-1,-1,-1)]
    return bytes(l)


def break_block(previous_block, current_block):
    known = []
    for offset in range(16):
        suffix = craft_suffix(previous_block, known, offset)
        for i in range(256):
            crafted_previous_block = craft_previous(bytes([i]), suffix)
            attempt = bytes(crafted_previous_block+current_block)
            if consume_token(attempt, iv):
                plaintext = cbc_decrypt(attempt, iv, global_key)
                last_byte_value = bytes([i ^ previous_block[15-offset] ^ (offset+1)])

                known.insert(0, last_byte_value)
                break
    return b''.join(known)

def break_ciphertext(ciphertext):
    index = 0
    plaintext = bytearray()
    while index < len(ciphertext):
        current_block = ciphertext[index:index+16]
        # I assume that we know the IV here.
        previous_block = ciphertext[index-16:index] if index != 0 else iv

        broken = break_block(previous_block, current_block)
        plaintext += broken
        index += 16
    return bytes(plaintext)

if __name__ == '__main__':
    global_key = n_random_bytes(16)

    ciphertext, iv = generate_token(global_key)
    plaintext = cbc_decrypt(ciphertext, iv, global_key)
    print("Expected plaintext")
    offset = 0
    while(offset < len(plaintext)):
        print(bytes(plaintext[offset:offset+16]))
        offset += 16
    print(" ===== ")
    print(break_ciphertext(ciphertext))