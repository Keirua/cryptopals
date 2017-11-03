
My implementation of the solutions to [Matsumoto's crypto challenges](http://www.cryptopals.com/).

# Stuff I've learnt

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

 - [x] The CBC padding oracle
 - [x] Implement CTR, the stream cipher mode
 - [ ] Break fixed-nonce CTR mode using substitutions
 - [x] Break fixed-nonce CTR statistically
 - [x] Implement the MT19937 Mersenne Twister RNG
 - [x] Crack an MT19937 seed
    - with python then rust
 - [x] Clone an MT19937 RNG from its output
 - [x] Create the MT19937 stream cipher and break it

## Level 17

https://en.wikipedia.org/wiki/Padding_oracle_attack
https://github.com/neuhalje/aes_padding_oracle_attack

All the articles about the weakness explain the same thing, the general idea is not very hard, on paper I had the correct formulas anyway, the algorithm is only 50 lines long... and yet, it took me 2 evenings to correctly implement this attack.

## Level 20

Easy given that the hard part (breaking xor with repeating key using statistical analysis ) was done in set1. Reused the code.

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

# Set 4

 - [x] Break "random access read/write" AES CTR
 - [x] CTR bitflipping
 - [x] Recover the key from CBC with IV=Key
 - [x] Implement a SHA-1 keyed MAC
 - [ ] Break a SHA-1 keyed MAC using length extension
 - [ ] Break an MD4 keyed MAC using length extension
 - [x] Implement and break HMAC-SHA1 with an artificial timing leak
 - [x] Break HMAC-SHA1 with a slightly less artificial timing leak


## HMAC-SHA1

Simple timing attack, but pretty cool though !

	$ python level31_hmac.py
	The key hash is b'0a929740a40849a9906a6ff7796b3f5ef60af966030053aae6cba6513263ec0056944dadf54d3903842a6708dabca5888639a2bea9c35fa5dd72d9df537e4e9e'
	The computed hash is adbf605f30fea41b6611f77c45835fd98fa476c4
	50.220947265625 a
	100.552734375 d
	151.00732421875 b
	201.095947265625 f
	250.763427734375 6
	301.393310546875 0
	350.97265625 5
	401.712646484375 f
	452.179443359375 3
	502.0517578125 0
	551.902587890625 f
	602.562255859375 e
	652.865478515625 a
	702.506103515625 4
	752.42626953125 1
	802.69091796875 b
	853.024169921875 6
	903.249267578125 6
	954.131103515625 1
	1003.811279296875 1
	1053.411865234375 f
	1104.21826171875 7
	1153.592529296875 7
	1204.70849609375 c
	1255.463623046875 4
	1305.658447265625 5
	1355.065673828125 8
	1405.784912109375 3
	1455.9755859375 5
	1506.12939453125 f
	1555.75244140625 d
	1606.553955078125 9
	1656.902099609375 8
	1706.769775390625 f
	1757.3037109375 a
	1804.88134765625 4
	1856.85546875 7
	1908.12255859375 6
	1957.110107421875 c
	2004.29785156254
	The broken mac hash is adbf605f30fea41b6611f77c45835fd98fa476c4

## Level 32

Pretty cool to go down to 5 nanoseconds !
Elements that worked:

 - only run the timing process.
 - use statistical analysis to take multiple samples (10 were not enough) and remove outliers
 - Could be improved with more threads and a more efficient cpu usage.

time python level32_hmac_harder.py
Duration = 5e-06s
The key hash is b'f778af443d68c252128566a202e0217af9701e903a2d94814d9bd594db081a40f720e400172e5bcd1d978402ac434d9cddd28e72d9f66c967f8ef6ed5f673e4e'
The broken mac hash is 0c0d03d910ebfee7ae956d1759b2dd95114d2da3
The computed hash is 0c0d03d910ebfee7ae956d1759b2dd95114d2da3
They match !
python level32_hmac_harder.py  1,15s user 0,61s system 15% cpu 11,551 total