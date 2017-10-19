import unittest

class TestParseCookie(unittest.TestCase):
    def test_querystring_parse(self):
        s = "foo=bar&baz=qux&zap=zazzle"
        self.assertEqual({'baz': 'qux', 'foo': 'bar', 'zap': 'zazzle'}, querystring_parse(s))
        self.assertEqual({'a':'b'}, querystring_parse('a=b'))
        self.assertEqual({}, querystring_parse(''))
        self.assertEqual({}, querystring_parse('a'))

    def test_profile_for(self):
        self.assertEqual("email=bidou@plop.com&uid=10&role=user", profile_for("bidou@plop.com"))

    def test_profile_for_error(self):
        with self.assertRaises(ValueError):
            profile_for("abc&def")
        with self.assertRaises(ValueError):
            profile_for("foo=bar")

def querystring_parse(s):
    d = {}
    kvList = s.split('&')
    if len(kvList) > 0:
        for kv in [split.split('=') for split in kvList]:
            if(len(kv) == 2):
                d[kv[0]] = kv[1]
    return d

def profile_for(email):
    if ('&' in email or '=' in email):
        raise ValueError("& and = are not allowed in the input string")
    return "email={}&uid=10&role=user".format(email)


if __name__ == '__main__':
    unittest.main()

