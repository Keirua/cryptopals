import unittest

def querystring_parse(s):
    d = {}
    kvList = s.split('&')
    if len(kvList) > 0:
        for kv in [split.split('=') for split in kvList]:
            if(len(kv) == 2):
                d[kv[0]] = kv[1]
    return d

def profile_for(email):
    return "email={}&uid=10&role=user".format(email)

class TestParseCookie(unittest.TestCase):
    def test_nominal(self):
        s = "foo=bar&baz=qux&zap=zazzle"
        self.assertEqual({'baz': 'qux', 'foo': 'bar', 'zap': 'zazzle'}, querystring_parse(s))
        self.assertEqual({'a':'b'}, querystring_parse('a=b'))
        self.assertEqual({}, querystring_parse(''))
        self.assertEqual({}, querystring_parse('a'))

    def test_profile_for(self):
        self.assertEqual("email=bidou@plop.com&uid=10&role=user", profile_for("bidou@plop.com"))

if __name__ == '__main__':
    unittest.main()

