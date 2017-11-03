from cryptolib import hmac_sha1, n_random_bytes
from time import sleep, time
from binascii import hexlify

def verify(file, signature, sleep_time, key):
    mac = hmac_sha1(key, file)
    for (m1, m2) in zip(mac, signature):
        if(m1 != m2):
            return False
        sleep(sleep_time)
    return True

#print(verify(file, realmac) == True)
#print(verify(file, fakemac) == False)
#print(realmac)

def break_mac(file):
    mac = ''
    while len(mac) < 40:
        best_char = None
        highest_timing  = 0
        for c in '0123456789abcdef':
            t1 = time()
            verify(file, mac + c, 0.05, key)
            t2 = time()
            print(c, t2-t1)
            if (t2-t1) > highest_timing:
                highest_timing = t2-t1
                best_char = c
        mac += best_char
    return mac

if __name__ == '__main__':
    key = n_random_bytes(64)
    file = b"Some file content"

    fakemac = hmac_sha1(b"", file)
    realmac = hmac_sha1(key, file)

    print ("The key hash is {}".format(hexlify(key)))
    print ("The computed hash is {}".format(realmac))
    print ("The broken mac hash is {}".format(break_mac(file)))
