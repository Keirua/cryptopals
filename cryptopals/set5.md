# Crypto Challenge Set 5

This is the first set of number-theoretic cryptography challenges, and also our coverage of message authentication.

This set is significantly harder than the last set. The concepts are new, the attacks bear no resemblance to those of the previous sets, and... math.

On the other hand, our favorite cryptanalytic attack ever is in this set (you'll see it soon). We're happy with this set. Don't wimp out here. You're almost done! 

 - Implement Diffie-Hellman
 - Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection
 - Implement DH with negotiated groups, and break with malicious "g" parameters
 - Implement Secure Remote Password (SRP)
 - Break SRP with a zero key
 - Offline dictionary attack on simplified SRP
 - Implement RSA
 - Implement an E=3 RSA Broadcast attack

# Implement Diffie-Hellman

For one of the most important algorithms in cryptography this exercise couldn't be a whole lot easier.

Set a variable "p" to 37 and "g" to 5. This algorithm is so easy I'm not even going to explain it. Just do what I do.

Generate "a", a random number mod 37. Now generate "A", which is "g" raised to the "a" power mode 37 --- A = (g**a) % p.

Do the same for "b" and "B".

"A" and "B" are public keys. Generate a session key with them; set "s" to "B" raised to the "a" power mod 37 --- s = (B**a) % p.

Do the same with A**b, check that you come up with the same "s".

To turn "s" into a key, you can just hash it to create 128 bits of key material (or SHA256 it to create a key for encrypting and a key for a MAC).

Ok, that was fun, now repeat the exercise with bignums like in the real world. Here are parameters NIST likes:

p:
ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024
e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec
6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f
24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361
c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552
bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff
fffffffffffff
 
g: 2

This is very easy to do in Python or Ruby or other high-level languages that auto-promote fixnums to bignums, but it isn't "hard" anywhere.

Note that you'll need to write your own modexp (this is blackboard math, don't freak out), because you'll blow out your bignum library raising "a" to the 1024-bit-numberth power. You can find modexp routines on Rosetta Code for most languages.




# Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection

Use the code you just worked out to build a protocol and an "echo" bot. You don't actually have to do the network part of this if you don't want; just simulate that. The protocol is:

A->B
    Send "p", "g", "A"
B->A
    Send "B"
A->B
    Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
B->A
    Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv

(In other words, derive an AES key from DH with SHA1, use it in both directions, and do CBC with random IVs appended or prepended to the message).

Now implement the following MITM attack:

A->M
    Send "p", "g", "A"
M->B
    Send "p", "g", "p"
B->M
    Send "B"
M->A
    Send "p"
A->M
    Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
M->B
    Relay that to B
B->M
    Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
M->A
    Relay that to A

M should be able to decrypt the messages. "A" and "B" in the protocol --- the public keys, over the wire --- have been swapped out with "p". Do the DH math on this quickly to see what that does to the predictability of the key.

Decrypt the messages from M's vantage point as they go by.

Note that you don't actually have to inject bogus parameters to make this attack work; you could just generate Ma, MA, Mb, and MB as valid DH parameters to do a generic MITM attack. But do the parameter injection attack; it's going to come up again.

# Implement DH with negotiated groups, and break with malicious "g" parameters

A->B
    Send "p", "g"
B->A
    Send ACK
A->B
    Send "A"
B->A
    Send "B"
A->B
    Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
B->A
    Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv

Do the MITM attack again, but play with "g". What happens with:

    g = 1
    g = p
    g = p - 1

Write attacks for each.
When does this ever happen?
Honestly, not that often in real-world systems. If you can mess with "g", chances are you can mess with something worse. Most systems pre-agree on a static DH group. But the same construction exists in Elliptic Curve Diffie-Hellman, and this becomes more relevant there.

# Implement Secure Remote Password (SRP)

To understand SRP, look at how you generate an AES key from DH; now, just observe you can do the "opposite" operation an generate a numeric parameter from a hash. Then:

Replace A and B with C and S (client & server)
C & S
    Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
S

        Generate salt as random integer
        Generate string xH=SHA256(salt|password)
        Convert xH to integer x somehow (put 0x on hexdigest)
        Generate v=g**x % N
        Save everything but x, xH

C->S
    Send I, A=g**a % N (a la Diffie Hellman)
S->C
    Send salt, B=kv + g**b % N
S, C
    Compute string uH = SHA256(A|B), u = integer of uH
C

        Generate string xH=SHA256(salt|password)
        Convert xH to integer x somehow (put 0x on hexdigest)
        Generate S = (B - k * g**x)**(a + u * x) % N
        Generate K = SHA256(S)

S

        Generate S = (A * v**u) ** b % N
        Generate K = SHA256(S)

C->S
    Send HMAC-SHA256(K, salt)
S->C
    Send "OK" if HMAC-SHA256(K, salt) validates

You're going to want to do this at a REPL of some sort; it may take a couple tries.

It doesn't matter how you go from integer to string or string to integer (where things are going in or out of SHA256) as long as you do it consistently. I tested by using the ASCII decimal representation of integers as input to SHA256, and by converting the hexdigest to an integer when processing its output.

This is basically Diffie Hellman with a tweak of mixing the password into the public keys. The server also takes an extra step to avoid storing an easily crackable password-equivalent.


# Break SRP with a zero key

Get your SRP working in an actual client-server setting. "Log in" with a valid password using the protocol.

Now log in without your password by having the client send 0 as its "A" value. What does this to the "S" value that both sides compute?

Now log in without your password by having the client send N, N*2, &c.
Cryptanalytic MVP award

Trevor Perrin and Nate Lawson taught us this attack 7 years ago. It is excellent. Attacks on DH are tricky to "operationalize". But this attack uses the same concepts, and results in auth bypass. Almost every implementation of SRP we've ever seen has this flaw; if you see a new one, go look for this bug.

# Offline dictionary attack on simplified SRP
S

x = SHA256(salt|password)
    v = g**x % n

C->S

I, A = g**a % n

S->C

salt, B = g**b % n, u = 128 bit random number

C

x = SHA256(salt|password)
    S = B**(a + ux) % n
    K = SHA256(S)

S

S = (A * v ** u)**b % n
    K = SHA256(S)

C->S
Send HMAC-SHA256(K, salt)
S->C
Send "OK" if HMAC-SHA256(K, salt) validates

Note that in this protocol, the server's "B" parameter doesn't depend on the password (it's just a Diffie Hellman public key).

Make sure the protocol works given a valid password.

Now, run the protocol as a MITM attacker: pose as the server and use arbitrary values for b, B, u, and salt.

Crack the password from A's HMAC-SHA256(K, salt).

# Implement RSA

There are two annoying things about implementing RSA. Both of them involve key generation; the actual encryption/decryption in RSA is trivial.

First, you need to generate random primes. You can't just agree on a prime ahead of time, like you do in DH. You can write this algorithm yourself, but I just cheat and use OpenSSL's BN library to do the work.

The second is that you need an "invmod" operation (the multiplicative inverse), which is not an operation that is wired into your language. The algorithm is just a couple lines, but I always lose an hour getting it to work.

I recommend you not bother with primegen, but do take the time to get your own EGCD and invmod algorithm working.

Now:

    Generate 2 random primes. We'll use small numbers to start, so you can just pick them out of a prime table. Call them "p" and "q".
    Let n be p * q. Your RSA math is modulo n.
    Let et be (p-1)*(q-1) (the "totient"). You need this value only for keygen.
    Let e be 3.
    Compute d = invmod(e, et). invmod(17, 3120) is 2753.
    Your public key is [e, n]. Your private key is [d, n].
    To encrypt: c = m**e%n. To decrypt: m = c**d%n
    Test this out with a number, like "42".
    Repeat with bignum primes (keep e=3).

Finally, to encrypt a string, do something cheesy, like convert the string to hex and put "0x" on the front of it to turn it into a number. The math cares not how stupidly you feed it strings.


# Implement an E=3 RSA Broadcast attack

Assume you're a Javascript programmer. That is, you're using a naive handrolled RSA to encrypt without padding.

Assume you can be coerced into encrypting the same plaintext three times, under three different public keys. You can; it's happened.

Then an attacker can trivially decrypt your message, by:

    Capturing any 3 of the ciphertexts and their corresponding pubkeys
    Using the CRT to solve for the number represented by the three ciphertexts (which are residues mod their respective pubkeys)
    Taking the cube root of the resulting number

The CRT says you can take any number and represent it as the combination of a series of residues mod a series of moduli. In the three-residue case, you have:

result =
  (c_0 * m_s_0 * invmod(m_s_0, n_0)) +
  (c_1 * m_s_1 * invmod(m_s_1, n_1)) +
  (c_2 * m_s_2 * invmod(m_s_2, n_2)) mod N_012

where:

 c_0, c_1, c_2 are the three respective residues mod
 n_0, n_1, n_2

 m_s_n (for n in 0, 1, 2) are the product of the moduli
 EXCEPT n_n --- ie, m_s_1 is n_0 * n_2

 N_012 is the product of all three moduli

To decrypt RSA using a simple cube root, leave off the final modulus operation; just take the raw accumulated result and cube-root it.
