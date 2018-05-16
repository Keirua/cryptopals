import socket
from cryptolib import read_int, send_int
from random import randint, shuffle
import struct
from time import sleep

# https://stackoverflow.com/questions/33913308/socket-module-how-to-send-integer
primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199
]

p = primes[randint(0, len(primes)-1)]
g = primes[randint(0, len(primes)-1)]
a = randint(1, 1024)

A = pow(g,a,p)

with open("/usr/share/dict/words", 'r') as f:
    words = [ w.strip() for w in f.readlines() if 6 <= len(w) <= 10 ]
    
def generate_message(nb_words=3):
    shuffle(words)
    return (" - ".join(words[:nb_words]))

secret_message = generate_message()
print("Our secret message = {}".format(secret_message))

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 5000
     
    mySocket = socket.socket()
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    #data = conn.recv(1024).decode()
    send_int(conn, p)
    send_int(conn, g)
    send_int(conn, A)
    print("[SEND] p, g, A = {}, {}, {}".format(p, g, A))

    B = read_int(conn)
    print("[RECV] B = {}".format(B))

    sleep(0.5)
    conn.close()