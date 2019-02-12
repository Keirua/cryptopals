from level31_hmac import verify
from cryptolib import hmac_sha1, n_random_bytes
from time import sleep, time
from binascii import hexlify
import statistics

key = n_random_bytes(64)
duration = 5e-6

def break_mac_harder(file):
    mac = ''
    nb_iterations = 15

    while len(mac) < 40:
        best_char = None
        highest_timing  = 0

        timings = {}
        for i in range(nb_iterations):
            for c in '0123456789abcdef':
                t1 = time() * 1000
                verify(file, mac + c, duration, key)
                t2 = time() * 1000

                timings[c] = [] if c not in timings else timings[c]
                timings[c].append(t2-t1)

        for k in timings:
            m = statistics.mean(timings[k])
            sd = statistics.stdev(timings[k])

            # remove outliers
            final_list = [x for x in timings[k] if (abs(x-m) < 2 * sd)]
            a = sum(final_list)/len(final_list)
            if a > highest_timing:
                highest_timing = a
                best_char = k

        mac += best_char

    return mac


file = b"Some file content"

realmac = hmac_sha1(key, file)
print ("The key hash is {}".format(hexlify(key)))
broken_mac = break_mac_harder(file)
print ("The broken mac hash is {}".format(broken_mac))
print ("The computed hash is   {}".format(realmac))

print("They match !" if realmac == broken_mac else "They differ :(")