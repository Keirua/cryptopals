class mt32:
    lower_mask = 0x7fffffff
    upper_mask = 0x80000000

    def __init__(self, seed):
        self.index = 625
        self.MT = [0 for i in range(0, 625)]
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = int(0xFFFFFFF & (1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i))

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9d2c5680)
        y = y ^ ((y << 15) & 0xefc60000)
        y = y ^ (y >> 18)

        self.index += 1
        return int(y & 0xFFFFFFF)

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

m = mt32(1234)

for i in range (10):
    print(m.extract_number())
