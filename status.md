
# stuff I've learnt

 - the modes of operation for a block cipher, their weaknesses, some attacks against them
 - python, rust. Got better.
 - frequency analysis
 - dictionnary attack
 - timing attack
 - input crafting
 - binary operations
 - When there's no solution, there's still bruteforce :)
 - [Endianness](https://betterexplained.com/articles/understanding-big-and-little-endian-byte-order/)

# Set 1

 - [x] Convert hex to base64
 - [x] Fixed XOR
 - [x] Single-byte XOR cipher
 	- done using wordlist for matching
 	- done using scoring based on frequency
 - [x] Detect single-character XOR
 - [x] Implement repeating-key XOR
 - [x] Break repeating-key XOR
 - [x] AES in ECB mode
 - [x] Detect AES in ECB mode

Tried chi squared method for ranking, didn't work well due to the non ascii characters

https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis

# Set 2

 - [x] Implement PKCS#7 padding
 - [x] Implement CBC mode
 - [x] An ECB/CBC detection oracle
 - [x] Byte-at-a-time ECB decryption (Simple)
 - [ ] ECB cut-and-paste
 - [x] Byte-at-a-time ECB decryption (Harder)
 - [x] PKCS#7 padding validation
 - [x] CBC bitflipping attacks

Great set, cleverly built. 2 timing attacks, beating the hard one feels awesome.
Crafting payload for the cbc bitflipping attack was pretty fun too.

# Set 3

 - [ ] The CBC padding oracle
 - [x] Implement CTR, the stream cipher mode
 - [ ] Break fixed-nonce CTR mode using substitutions
 - [ ] Break fixed-nonce CTR statistically
 - [x] Implement the MT19937 Mersenne Twister RNG
 - [x] Crack an MT19937 seed
    - with python then rust
 - [ ] Clone an MT19937 RNG from its output
 - [ ] Create the MT19937 stream cipher and break it

## Level 21

In order to check that the mersenne twister works as expected, diff its output with the output of the original algorithm:

$ gcc mt19937.c -o mt19937
$ diff <(python level21_mt19937.py 2342 15) <(./mt19937 2342 15)

## Level 22

Attempted to bruteforce it. Python was not a good idea (it only tries  like 1000 seeds/s). Rust quickly proved to be able to find the seed in a reasonnable time (~1H), which is about 100x faster. 

If you wanna do bruteforce, you'd better do it with a fast language :)

	$ time target/release/crack_mt32seed ~/dev/cryptopals/set3/mt32/1508440814.mt32
	...
	1499000000
	1500000000
	1501000000
	1502000000
	1503000000
	1504000000
	1505000000
	1506000000
	1507000000
	1508000000
	1508440814 is the seed's value
	target/release/crack_mt32seed ~/dev/cryptopals/set3/mt32/1508440814.mt32  3277,82s user 0,95s system 99% cpu 54:38,87 total

