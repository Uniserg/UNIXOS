import socket
from crypt import *
from key import Key


def get_addr() -> tuple:
    host = str(input("Enter host: "))
    if host == '' or host is None:
        host = "localhost"

    while True:
        port = int(input("Enter port: "))
        if 0 < port < 65535:
            break
        else:
            print("Incorrect port string")

    return host, port


def create_client_keys():
    key = Key(create_param(), create_param(), create_param())

    write_key("private_key_server.pem", key.private_key)
    write_key("private_key_server.pem", key.private_key)


def key_exchange(sock) -> tuple[int, int]:
    client_public_key = read_key("public_key_client.pem")
    sock.send(client_public_key.encode('utf-8'))
    print("Sent client public key to the server: " + client_public_key.replace('\n', " "))

    B_attr_server = sock.recv(2048).decode('utf-8')
    print("Received server B attribute key: " + B_attr_server.replace('\n', " "))
    B_attr_server = B_attr_server.split('\n')
    client_private_key = read_key("private_key_client.pem").split('\n')

    server_public_key = sock.recv(2048).decode('utf-8')
    print("Received server public key: " + server_public_key.replace('\n', " "))

    server_public_key = server_public_key.split('\n')
    calc_key_server = Key(create_param(), int(server_public_key[0]), int(server_public_key[1]))
    B_attr_client = str(calc_key_server.AB) + '\n'
    sock.send(B_attr_client.encode('utf-8'))
    print("Sent client B attribute to the server: " + B_attr_client.replace('\n', " "))

    client_private_key = read_key("private_key_client.pem").split('\n')
    client_public_key = client_public_key.split('\n')

    K_client = create_sym_key(int(client_private_key[0]), int(B_attr_server[0]), int(client_public_key[1]))
    print('Calculated common private key for client: ' + str(K_client))
    K_server = create_sym_key(calc_key_server.ab, int(server_public_key[2]), calc_key_server.p)
    print('Calculated common private key for the server: ' + str(K_server))

    return K_client, K_server


def client_performance():
    sock = socket.socket()
    host, port = get_addr()

    sock.connect((host, port))
    print("Connected to the server")

    create_client_keys()
    K_client, K_server = key_exchange(sock)
    starting = sock.recv(2048).decode('utf-8')
    if starting == "Server is ready":
        pass

    while True:
        message = cipher(str(K_client), str(input("Enter a new message: ")))
        sock.send(message.encode('utf-8'))

        response = cipher(str(K_server), sock.recv(2048).decode('utf-8'))
        print("Received a new message:", response)

        if response == 'end':
            break

    sock.close()
    print("Disconnecting the client from the server")


if __name__ == "__main__":
    client_performance()
