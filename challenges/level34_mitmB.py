import socket
from cryptolib import read_int, send_int
from random import randint
import struct


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
     
    mySocket = socket.socket()
    mySocket.connect((host,port))
         
    p = read_int(mySocket)
    g = read_int(mySocket)
    A = read_int(mySocket)

    b = randint(1, 1024)
    B = pow(g, b, p)

    print("[RECV] p, g, A = {}, {}, {}".format(p, g, A))

    send_int(mySocket, B)
    print("[SEND] B = {}".format(B))

    mySocket.close()