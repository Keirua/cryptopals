import unittest

def pkcs(s:str, block_size: int) -> str:
    remainder = len(s) % block_size
    if remainder == 0:
        return s
    return s + bytes([block_size-remainder for i in range(block_size-remainder)])

print(pkcs(b"YELLOW SUBMARINE", 8))
print(pkcs(b"YELLOW SUBMARINE", 20))

class TestPkcs(unittest.TestCase):
    def test_main(self):
        s = b"YELLOW SUBMARINE"
        self.assertEqual(s, pkcs(s, 8))
        self.assertEqual(b"YELLOW SUBMARINE\x04\x04\x04\x04", pkcs(s, 20))

        s = b"abcd"
        self.assertEqual(b"abcd\x04\x04\x04\x04", pkcs(s, 8))
        self.assertEqual(b"abcd\x03\x03\x03", pkcs(s, 7))
        self.assertEqual(b"abcd\x06\x06\x06\x06\x06\x06", pkcs(s, 10))
        self.assertEqual(b"abcd", pkcs(s, 2))
        self.assertEqual(b"abcd", pkcs(s, 4))

if __name__ == '__main__':
    unittest.main()    	