import unittest

def pkcs_strip(s):
    if(len(s) <= 0):
        return s
    l = s[len(s)-1]
    if (l in range(1,16)):
        for i in range(1, l+1):
            if s[len(s)-i] != l:
                raise ValueError("Not a pkcs-padded string : {}".format(s))
        return s[:len(s)-l]
    return s

class TestPkcs(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY\x04\x04\x04\x04"))
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY\x05\x05\x05\x05\x05"))
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F"))
        self.assertEqual(b"ICE ICE BABY", pkcs_strip(b"ICE ICE BABY"))
        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY\x05\x05\x05\x05")
        with self.assertRaises(ValueError):
            pkcs_strip(b"ICE ICE BABY\x01\x02\x03")

if __name__ == '__main__':
    unittest.main()