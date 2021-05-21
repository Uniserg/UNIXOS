import socket
import threading
from crypt import *
from key import Key


threads = []


def create_server_keys():
    key = Key(create_param(), create_param(), create_param())
    write_key("private_key_server.pem", key.private_key)
    write_key("public_key_server.pem", key.public_key)


def key_exchange(conn) -> tuple[int, int]:
    client_public_key = conn.recv(2048).decode('utf-8')
    print("Received client public key: " + client_public_key.replace('\n', " "))

    client_public_key = client_public_key.split('\n')
    calc_key_client = Key(create_param(), int(client_public_key[0]), int(client_public_key[1]))
    B_attr_server = str(calc_key_client.AB) + '\n'
    conn.send(B_attr_server.encode('utf-8'))
    print("Sent server B attribute to the client: " + B_attr_server.replace('\n', " "))

    server_public_key = read_key("public_key_server.pem")
    conn.send(server_public_key.encode('utf-8'))
    print('Sent server public key to the client: ' + server_public_key.replace('\n', " "))

    B_attr_client = conn.recv(2048).decode('utf-8')
    print("Received client B attribute key: " + B_attr_client.replace('\n', " "))
    B_attr_client = B_attr_client.split('\n')

    server_private_key = read_key("private_key_server.pem").split('\n')
    server_public_key = server_public_key.split('\n')

    K_client = create_sym_key(calc_key_client.ab, int(client_public_key[2]), calc_key_client.p)
    print('Calculated common private key for the client: ' + str(K_client))
    K_server = create_sym_key(int(server_private_key[0]), int(B_attr_client[0]), int(server_public_key[1]))
    print('Calculated common private key for the server: ' + str(K_server))

    return K_client, K_server


def get_addr() -> tuple:
    sock = socket.socket()
    print("Server is started")

    host = str(input("Enter host: "))
    if host == '' or host is None:
        host = "localhost"

    while True:
        port = int(input("Enter port: "))
        if 0 < port < 65535:
            try:
                sock.bind((host, port))
                break
            except OSError:
                print(f"Port {port} in used")
        else:
            print("Incorrect port string")

    return sock, port


def sender(conn, K_client: str, K_server: str):
    conn.send("Server is ready".encode('utf-8'))
    while True:
        message = cipher(K_client, conn.recv(2048).decode('utf-8'))
        print("Received message from the client:", message)

        conn.send(cipher(K_server, message).encode('utf-8'))
        print("Sent message to the client:", message)

        if message == 'end':
            print("The client disconnected")
            break


def server_performance():
    global threads

    sock, port = get_addr()
    sock.listen(1000)
    print("Listening port: " + str(port))

    while True:
        conn, addr = sock.accept()
        print("Client connected:", str(addr))

        create_server_keys()
        K_client, K_server = key_exchange(conn)

        thread = threading.Thread(target=sender, name="Sender", args=[conn, str(K_client), str(K_server)])
        threads.append(thread)
        thread.start()

    sock.close()
    print("Stop the server")


if __name__ == "__main__":
    server_performance()
