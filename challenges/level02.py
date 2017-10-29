import base64
import binascii

# 1c0111001f010100061a024b53535009181c
# ... after hex decoding, and when XOR'd against:
# 686974207468652062756c6c277320657965
# ... should produce:
# 746865206b696420646f6e277420706c6179

a1 = b"1c0111001f010100061a024b53535009181c"
a2 = b"686974207468652062756c6c277320657965"

hex_a1 = binascii.unhexlify(a1)
hex_a2 = binascii.unhexlify(a2)


hex_xor = bytes([hex_a1[i] ^ hex_a2[i] for i in range(len(hex_a1))])
expected_xor= b"746865206b696420646f6e277420706c6179"
print(binascii.hexlify(hex_xor) == expected_xor)
print(hex_xor)