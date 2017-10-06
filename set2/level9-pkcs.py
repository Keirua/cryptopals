import unittest

def pkcs(s:str, block_size: int, padding: bytes) -> str:
	remainder = len(s) % block_size
	if remainder == 0:
		return s
	return s + padding * (block_size-remainder)

print(pkcs(b"YELLOW SUBMARINE", 8, b'\x04'))
print(pkcs(b"YELLOW SUBMARINE", 20, b'\x04'))

class TestPkcs(unittest.TestCase):
    def test_main(self):
    	s = b"YELLOW SUBMARINE"
    	self.assertEqual(s, pkcs(s, 8, b'\x04'))
    	self.assertEqual(b"YELLOW SUBMARINE\x04\x04\x04\x04", pkcs(s, 20, b'\x04'))

    	s = b"abcd"
    	self.assertEqual(b"abcd\x04\x04\x04\x04", pkcs(s, 8, b'\x04'))
    	self.assertEqual(b"abcd\x04\x04\x04", pkcs(s, 7, b'\x04'))
    	self.assertEqual(b"abcd", pkcs(s, 2, b'\x04'))
    	self.assertEqual(b"abcd", pkcs(s, 4, b'\x04'))

if __name__ == '__main__':
    unittest.main()    	