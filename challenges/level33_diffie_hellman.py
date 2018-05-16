from random import randint
from binascii import unhexlify
from hashlib import sha256

# The basic idea works like this:
# 
#  - I come up with two prime numbers g and p and tell you what they are.

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

# - You then pick a secret number (a), but you don't tell anyone.
# Instead you compute g**a mod p and send that result back to me.
# (We'll call that A since it came from a).

max_value = 1024
a = randint(1, 1024)

 # A & B are public keys
A = pow(g, a, p) # = (g ** a) % p

#  - I do the same thing, but we'll call my secret number b and
# the computed number B. So I compute g**b mod p and send you the
# result (called "B")
b = randint(1, 1024)
B = pow(g, b, p)

#  - Now, you take the number I sent you and do the exact same
# operation with it. So that's B**a mod p.
sB = (B ** a) % p
#  - I do the same operation with the result you sent me,
# so: A**b mod p.
sA = (A ** b) % p
# sA and sB are equal due to a property of modular exponentiation
print(sB == sA)

print(a, b)
print("A = {}".format(A))
print("B = {}".format(B))
print("s = {}".format(sA))
print("sha256(s) = {}".format(sha256(s).hexdigest()))
