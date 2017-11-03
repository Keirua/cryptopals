from cryptolib import hmac_sha1, n_random_bytes
from time import sleep, time
from binascii import hexlify

def verify(file, signature):
    mac = hmac_sha1(key, file)
    for (m1, m2) in zip(mac, signature):
        if(m1 != m2):
            return False
        sleep(0.05)
    return True

key = n_random_bytes(64)
file = b"Some file content"

fakemac = hmac_sha1(b"", file)
realmac = hmac_sha1(key, file)

#print(verify(file, realmac) == True)
#print(verify(file, fakemac) == False)
#print(realmac)

def break_mac(file):
	mac = ''
	while len(mac) < 40:
	    for c in '0123456789abcdef':
	        t1 = time() * 1000
	        verify(file, mac + c)
	        t2 = time() * 1000
	        if (t2-t1 < 25+50*len(mac)):
	            continue
	        else:
	            mac += c
	            print(t2-t1, c)
	            break
	return mac

print ("The key hash is {}".format(hexlify(key)))
print ("The computed hash is {}".format(realmac))
print ("The broken mac hash is {}".format(break_mac(file)))
