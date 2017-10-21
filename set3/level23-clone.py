from random import randint
import itertools

def tamper(y):
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & 0x9d2c5680)
    y = y ^ ((y << 15) & 0xefc60000)
    y = y ^ (y >> 18)
    return y

def untamper(z):
    #z = (z & 0b11111111111111111100000000000000) + ((z ^ (z >> 18)) & 0b00000000000000000011111111111111)
    #z = (z & 0b00000000000000000111111111111111) + ((z ^ ((z << 15) & 0xefc60000)) & 0b11111111111111111000000000000000)
    z ^= (z >> 18)
    z ^= ((z << 15) & 0xefc60000)
    z ^= (z << 7) & 0x9d2c5680 & 0b00000000000000000011111110000000
    z ^= (z << 7) & 0x9d2c5680 & 0b00000000000111111100000000000000
    z ^= (z << 7) & 0x9d2c5680 & 0b00001111111000000000000000000000
    z ^= (z << 7) & 0x9d2c5680 & 0b11110000000000000000000000000000
    z ^= (z >> 11) & 0b11111111110000000000000000000000
    z ^= (z >> 11) & 0b00000000001111111111100000000000
    z ^= (z >> 11) & 0b00000000000000000000011111111111

    return z

import sys

class mt32:
    lower_mask = 0x7fffffff
    upper_mask = 0x80000000

    def __init__(self, seed=0):
        self.index = 625
        self.MT = [0 for i in range(0, 625)]
        self.MT[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            self.MT[i] = (0xFFFFFFFF & (1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i))

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9d2c5680)
        y = y ^ ((y << 15) & 0xefc60000)
        y = y ^ (y >> 18)

        self.index += 1
        return int(y & 0xFFFFFFFF)

    def twist(self):
        mag01 = [0, 0x9908b0df]
        for i in range(624-397):
            y = (self.MT[i] & self.upper_mask)|(self.MT[i+1] & self.lower_mask)
            self.MT[i] = self.MT[i + 397] ^ (y >> 1) ^ mag01[y & 1]
        for i in range(624-397, 624):
            y = (self.MT[i] & self.upper_mask)|(self.MT[i+1] & self.lower_mask)
            self.MT[i] = self.MT[i + (397-624)] ^ (y >> 1) ^ mag01[y & 1]
        y = (self.MT[624-1]&self.upper_mask)|(self.MT[0]&self.lower_mask)
        self.MT[624-1] = self.MT[396] ^ (y >> 1) ^ mag01[y & 1];
        self.index = 0

    @classmethod
    def cloneMT(self, values624):
        if(len(values624) != 624):
            raise ValueError("We need 624 values, {} give".format(len(values624)))

        clone = mt32()
        for i in range(len(values624)):
            clone.MT[i] = untamper(values624[i])
        clone.index = 625
        return clone

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python {} seed".format(sys.argv[0]))
        exit(1)

    # Let's create 624 random values with the original generator
    seed = int(sys.argv[1])
    m = mt32(seed)
    values = [m.extract_number() for _ in range(624)]

    # Now we can clone it and compare it's output
    c = mt32.cloneMT(values)
    for _ in range (10):
        print(c.extract_number() == m.extract_number())
