import socket
import pickle

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = conn.recv(1024)
print(pickle.loads(msg))

conn.close()
