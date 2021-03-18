import socket

sock = socket.socket()
sock.setblocking(1)
sock.connect(('localhost', 9090))
msg = "Hi!"
sock.send(msg.encode())

data = sock.recv(1024)

sock.close()

print(data.decode())
