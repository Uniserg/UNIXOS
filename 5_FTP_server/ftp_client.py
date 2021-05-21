import socket
import threading


class Client:
    def __init__(self):
        self.sock = None
        self.stop = True

    def start_client(self):
        self.stop = False

        while True:
            self.connect_to()
            listening = threading.Thread(name='listening-sock', target=self.listen_server_sock_data)
            sending = threading.Thread(name='sending-data', target=self.send_to_server)

            listening.start()
            sending.start()

            listening.join()
            sending.join()

            if self.stop:
                break

    def _check_connect(func):
        def wrapper(self, *params):
            try:
                func(self, *params)
            except (OSError, AttributeError):
                self.close_sock()

        return wrapper

    def _check_input(self, message=''):
        a = input(message)
        if a == '/stop' or a == '/exit':
            self.close_sock()
            self.stop = True

        elif a == '/disconnect':
            self.close_sock()
        return a

    def close_sock(self):
        if self.sock is not None:
            print(f'Соединение с {self.sock.getpeername()} потеряно!')
            self.sock.close()
            self.sock = None

    def connect_to(self):
        print('Давайте подключимся... ')
        while True:
            host = self._check_input("Введите имя хоста: ")
            try:
                port = int(self._check_input(f"Введите порт для {host}: "))
            except ValueError:
                print("Неверно указан адрес! Попробуйте еще раз!")
                continue

            self.sock = socket.socket()
            self.sock.setblocking(True)

            try:
                self.sock.connect((host, port))
                print(f"Подключение к {host}:{port} успешно!\n")
                break
            except (socket.gaierror, ConnectionRefusedError) as e:
                print(f"Не удается подключиться к {host}:{port} ({e})!")

    @_check_connect
    def listen_server_sock_data(self):
        while True:
            data = self.sock.recv(1024).decode()
            print(data)

    @_check_connect
    def send_to_server(self):
        while True:
            input_data = self._check_input()
            self.sock.send(input_data.encode())


if __name__ == '__main__':
    Client().start_client()
