import unittest
from base64 import b64decode
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
from random import randint
import hashlib
import socket
import struct


# Implementation of PKCS7
# https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7
def pkcs(s: str, block_size: int) -> str:
    remainder = len(s) % block_size
    return s + bytes([block_size - remainder for i in range(block_size - remainder)])


def pkcs_strip(s):
    if (len(s) <= 0):
        return s
    last_value = s[len(s) - 1]

    if (last_value not in range(1, 16 + 1)):
        raise ValueError("Not a pkcs-padded string : {}".format(s))

    for i in range(1, last_value + 1):
        if s[-i] != last_value:
            raise ValueError("Not a pkcs-padded string : {}".format(s))
    return s[:len(s) - last_value]


def aes_128_ecb_decrypt(ciphertext, key):
    aes_ecb128 = AES.new(key, AES.MODE_ECB)
    return aes_ecb128.decrypt(ciphertext)


def aes_128_ecb_encrypt(plaintext, key):
    aes_ecb128 = AES.new(key, AES.MODE_ECB)
    return aes_ecb128.encrypt(plaintext)


#  
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
    while (idx + block_size <= len(plaintext_padded)):
        current_plaintext = plaintext_padded[idx:idx + block_size]
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
    while (idx + block_size <= len(cipher_padded)):
        curr_block = cipher_padded[idx:idx + block_size]
        uncipher = aes_128_ecb_decrypt(curr_block, key)
        xored = xor_combine(uncipher, previous_cipher)
        out += xored
        previous_cipher = curr_block
        idx += block_size
    return out


def n_random_bytes(n=16):
    return bytes([randint(0, 255) for i in range(n)])


# Level 18

def create_input(nonce, counter):
    return bytes([
        (nonce & 0x00000000000000FF),
        (nonce & 0x000000000000FF00) >> 8,
        (nonce & 0x0000000000FF0000) >> 16,
        (nonce & 0x00000000FF000000) >> 24,
        (nonce & 0x000000FF00000000) >> 32,
        (nonce & 0x0000FF0000000000) >> 40,
        (nonce & 0x00FF000000000000) >> 48,
        (nonce & 0xFF00000000000000) >> 56,
        (counter & 0x00000000000000FF),
        (counter & 0x000000000000FF00) >> 8,
        (counter & 0x0000000000FF0000) >> 16,
        (counter & 0x00000000FF000000) >> 24,
        (counter & 0x000000FF00000000) >> 32,
        (counter & 0x0000FF0000000000) >> 40,
        (counter & 0x00FF000000000000) >> 48,
        (counter & 0xFF00000000000000) >> 56,
    ])


def aes_128_ctr(text, key, nonce):
    out = bytes()
    offset = 0
    counter = 0
    while offset < len(text):
        current_plaintext = text[offset:offset + 16]
        aesctr = aes_128_ecb_encrypt(create_input(nonce, counter), key)
        cipher = xor_combine(aesctr, current_plaintext)
        out += cipher
        counter += 1
        offset += 16
    return out


#  Level 31
# https://en.wikipedia.org/wiki/Hash-based_message_authentication_code
# SHA1-based HMAC
def hmac_sha1(key, message):
    if (len(key) > 64):
        key = hashlib.sha1(key).digest()  # keys longer than blocksize are shortened

    if (len(key) < 64):
        # keys shorter than blocksize are zero-padded
        key += b'\x00' * (64 - len(key))

    o_key_pad = xor_combine(b'\x5c' * 64, key)
    i_key_pad = xor_combine(b'\x36' * 64, key)

    return hashlib.sha1(o_key_pad + hashlib.sha1(i_key_pad + message).digest()).hexdigest()


class TestHMAC_SHA1(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual("fbdb1d1b18aa6c08324b7d64b71fb76370690e1d", hmac_sha1(b"", b""))
        self.assertEqual("de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9",
                         hmac_sha1(b"key", b"The quick brown fox jumps over the lazy dog"))


class TestPkcs(unittest.TestCase):
    def test_main(self):
        s = b"YELLOW SUBMARINE"
        self.assertEqual(b"YELLOW SUBMARINE\x08\x08\x08\x08\x08\x08\x08\x08", pkcs(s, 8))
        self.assertEqual(b"YELLOW SUBMARINE\x04\x04\x04\x04", pkcs(s, 20))

        s = b"abcd"
        self.assertEqual(b"abcd\x04\x04\x04\x04", pkcs(s, 8))
        self.assertEqual(b"abcd\x03\x03\x03", pkcs(s, 7))
        self.assertEqual(b"abcd\x06\x06\x06\x06\x06\x06", pkcs(s, 10))
        self.assertEqual(b"abcd\x02\x02", pkcs(s, 2))
        self.assertEqual(b"abcd\x04\x04\x04\x04", pkcs(s, 4))


class TestPkcsStrip(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY\x01"))
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY\x04\x04\x04\x04"))
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY\x05\x05\x05\x05\x05"))
        self.assertEqual(b"ICE ICE BABY",
                         pkcs_strip(b"ICE ICE BABY\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F"))

        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY\x00")
        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY")
        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY\x05\x05\x05\x05")
        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY\x01\x02\x03")
        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11")


def send_int(tcpsocket, ival):
    tcpsocket.send(struct.pack('!i', ival))


def read_int(tcpsocket):
    buf = ''
    while len(buf) < 4:
        buf += str(tcpsocket.recv(8))
    return struct.unpack('!i', bytes(buf[:4], 'ascii'))[0]


if __name__ == '__main__':
    unittest.main()
