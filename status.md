
# stuff I've learnt

 - the modes of operation for a block cipher, their weaknesses, some attacks against them
 - python. Got better.
 - frequency analysis
 - dictionnary attack
 - timing attack
 - input crafting
 - binary operations

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

In order to check that the mersenne twister works as expected, diff its output with the output of the original algorithm:

$ gcc mt19937.c -o mt19937
$ diff <(python level21_mt19937.py 2342 15) <(./mt19937 2342 15)