import socket
import threading
import queue


class Client:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setblocking(True)
        # self.recv_pack = queue.Queue()
        self.threads = set()
        self.stop = True

    def start_client(self):
        self.stop = False

        self.connect_to()
        threading.Thread(name='listening-sock', target=self.listen_sock_server_recv_data).start()
        threading.Thread(name='sending-data', target=self.send_to_server).start()
        # threading.Thread(name='receiving-data', target=self.receive_data).start()

    def _stop_client(self):
        self.stop = True
        self.sock.close()

    def _check_connect(func):
        def wrapper(*params):
            try:
                func(*params)
            except OSError:
                exit()
        return wrapper

    def _input_check(self, message=''):
        a = input(message)
        if a == '/stop' or a == '/exit':
            self._stop_client()
        return a

    def connect_to(self):
        print('Давайте подключимся... ')
        while True:
            host = self._input_check("Введите имя хоста: ")
            try:
                port = int(self._input_check(f"Введите порт для {host}: "))
            except ValueError:
                print("Неверно указан адрес! Попробуйте еще раз!")
                continue

            try:
                self.sock.connect((host, port))
                print(f"Подключение к {host}:{port} успешно!\n")
                break
            except (socket.gaierror, ConnectionRefusedError) as e:
                print(f"Не удается подключиться к {host}:{port} ({e})!")

    # @_check_connect
    # def receive_data(self):
    #     while True:
    #         if not self.recv_pack.empty():
    #             print(self.recv_pack.get())

    @_check_connect
    def listen_sock_server_recv_data(self):
        while True:
            data = self.sock.recv(1024).decode()
            print(data)
            # self.recv_pack.put(data)

    @_check_connect
    def send_to_server(self):
        while True:
            input_data = self._input_check()
            self.sock.send(input_data.encode())
            # if not self.recv_pack.empty():
            #     self.sock.send(input_data.encode())


if __name__ == '__main__':
    Client().start_client()
