import socket


def input_check(message=''):
    a = input(message)
    if a == '/stop' or a == '/exit':
        exit()

    return a


while True:
    while True:
        host = input_check("Введите имя имя хоста: ")
        try:
            port = int(input_check(f"Введите порт для {host}: "))
        except ValueError:
            print("Неверно указан порт! Попробуйте еще раз!")
            continue

        try:
            sock = socket.socket()
            sock.setblocking(True)
            sock.connect((host, port))
            print(f"Подключение к {host}:{port} успешно!\n")
            break
        except (socket.gaierror, ConnectionRefusedError) as e:
            print(f"Не удается подключиться к {host}:{port} ({e})!")

    while True:
        try:
            data = sock.recv(1024)
            print(data.decode())

            msg = input_check("=>")

            if msg == '':
                msg = 'None'

            if msg == '/close':
                print(f"Отключение от {host}:{port}\n")
                sock.shutdown(0)
                break
            sock.send(msg.encode())
        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as e:
            print(e)
            break

    sock.close()


