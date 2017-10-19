use std::env;
use std::fs::File;
use std::io::prelude::*;

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
}

fn read_values_from_file(filename:&str) -> Vec<u64> {
	let mut f = File::open(filename).expect("file not found");

    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");
    let values = contents.split("\n");
    let mut v = Vec::new();

    for value in values {
    	match value.parse::<u64>() {
    		Ok(n) => {
    			v.push(n);
    		},
    		_ => {  }
    	}
    }
   return v;
}

fn compare_by_seed(seed:u64, values: &Vec<u64>) -> bool {
	let mut m = Mt32::new(seed);
	for i in 0..values.len() {
		if m.extract_number() != values[i] {
			return false;
		}
	}
	return true;
}

fn main() {
	let args: Vec<_> = env::args().collect();
    if args.len() != 2 {
        println!("usage: {} filename", &args[0]);
    }

    println!("Loading file {}", &args[1]);
    let v = read_values_from_file(&args[1]);
    
    if v.len() != 32 {
    	println!("Not enough random numbers ! {:?}", v.len());
    	return;
    }

    // Benchmark with known values shows that it takes 18s to process
    // 1508440814 - 1500000000 = 8.4 millions values
    // in release
    // Starting from 0, that would mean about 30mn of processing
    // for i in 1500000000..1<<32 {
    for i in 0..1<<32 {
    	if compare_by_seed(i, &v) {
    		println!("{:?} is the seed's value", i);
    		break;
    	}
    	if (i % 1000000) == 0 {
    		println!("{:?}", i);
    	}
    }
}