import socket
import pickle

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.connect((HOST, PORT))

p, g, a = 7, 5, 3
A = g ** a % p
sock.send(pickle.dumps((p, g, A)))

sock.close()
