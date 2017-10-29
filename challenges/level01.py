import base64
import binascii

hex_str = b"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
expected_base64_str = b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

def hex_bytes_to_b64(hex_bytes):
	return base64.b64encode(binascii.unhexlify(hex_str))

def b64_to_hex_bytes(b64):
	return binascii.hexlify(base64.b64decode(expected_base64_str))

print(hex_bytes_to_b64(hex_str) == expected_base64_str)
print(b64_to_hex_bytes(expected_base64_str) == hex_str)