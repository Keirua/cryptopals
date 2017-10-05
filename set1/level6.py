from binascii import hexlify

a = "this is a test"
b = "wokka wokka!!!"

def different_bits(a, b):
	return sum((ord(a) & (1 << i)) != (ord(b) & (1 << i)) for i in range(0, 8))

def hamming(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(different_bits(el1, el2) for el1, el2 in zip(s1, s2))

print(hexlify(b'a'))
print(hexlify(b'b'))
print(hamming(a, b))
