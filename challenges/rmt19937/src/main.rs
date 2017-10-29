
struct Mt32 {
	index: i32,
	mt: [u64;624]
}

impl Mt32 {
	pub fn new(seed: u64) -> Mt32 {
		let mut m : Mt32 = Mt32 {
			index: 625,
			mt: [0; 624]
		};
    	m.mt[0] = seed & 0xFFFFFFFFu64;
    	for i in 1..624 {
            m.mt[i] = 0xFFFFFFFFu64 & (1812433253u64 * (m.mt[i-1] ^ (m.mt[i-1] >> 30)) + (i as u64));
    	}

		return m;
	}

	pub fn extract_number(&mut self) -> u64 { 
        if self.index >= 624 {
            self.twist();
        }

        let mut y: u64 = self.mt[self.index as usize];
        y = y ^ (y >> 11u64);
        y = y ^ ((y << 7u64) & 0x9d2c5680u64);
        y = y ^ ((y << 15u64) & 0xefc60000u64);
        y = y ^ (y >> 18u64);

        self.index += 1;
        return y & 0xFFFFFFFFu64
    }

    pub fn twist(&mut self) { 
        let mag01 = vec![0u64, 0x9908b0dfu64];
        let mut y:u64;
        for i in 0..(624-397) {	
            y = (self.mt[i] & 0x80000000u64)|(self.mt[i+1] & 0x7fffffffu64);
        	self.mt[i] = self.mt[i + 397] ^ (y >> 1u64) ^ mag01[(y & 1u64) as usize];
        }
        for i in (624-397)..624-1 {
            y = (self.mt[i] & 0x80000000u64)|(self.mt[i+1] & 0x7fffffffu64);
            self.mt[i] = self.mt[(i as i32 + (397i32-624i32)) as usize] ^ (y >> 1u64) ^ mag01[(y & 1u64) as usize];
		}

		y = (self.mt[624-1]&0x80000000u64)|(self.mt[0]&0x7fffffffu64);
		self.mt[624-1] = self.mt[396] ^ (y >> 1u64) ^ mag01[(y & 1u64) as usize];
        self.index = 0;
    }

    pub fn untamper(v:u64) -> u64 {
        let mut z = v;
        z ^= z >> 18;
        z ^= z << 15 & 0xefc60000;
        z ^= (z << 7) & 0x9d2c5680 & 0b00000000000000000011111110000000;
        z ^= (z << 7) & 0x9d2c5680 & 0b00000000000111111100000000000000;
        z ^= (z << 7) & 0x9d2c5680 & 0b00001111111000000000000000000000;
        z ^= (z << 7) & 0x9d2c5680 & 0b11110000000000000000000000000000;
        z ^= (z >> 11) & 0b11111111110000000000000000000000;
        z ^= (z >> 11) & 0b00000000001111111111100000000000;
        z ^= (z >> 11) & 0b00000000000000000000011111111111;
        return z;
    }

    pub fn clone(values624: Vec<u64>) -> Mt32 {
        let mut m : Mt32 = Mt32 {
            index: 625,
            mt: [0; 624]
        };
        for i in 0..624 {
            m.mt[i] = Mt32::untamper(values624[i]);
        }

        return m;
    }
}

fn main() {
	let mut m : Mt32 = Mt32::new(1234);

    let mut values = Vec::new();
    for _ in 0..624 {
        values.push(m.extract_number());
    }

    let mut c = Mt32::clone(values);
	for _ in 0..100 {
        let v_original = m.extract_number();
        let v_cloned = c.extract_number();
		println!("{}", v_original == v_cloned);
	}
}
