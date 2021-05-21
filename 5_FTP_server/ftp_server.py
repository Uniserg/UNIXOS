import socket
import threading
import logging
import sqlite3
import os

from datetime import datetime
from file_manager.filemanager import FileManager


class Server:
    def __init__(self, port=9090, bind_auto=False):
        self.port = port
        self.host = socket.gethostname()
        self.clients_conn = {}
        self.sock = socket.socket()
        self.sock.setblocking(True)
        self.db_conn = sqlite3.connect("chat.db", check_same_thread=False)
        self.cursor = self.db_conn.cursor()
        self.MAX_PORT = 10000
        self.MIN_PORT = 5000
        self.MAX_QUEUE = 1000
        self.autobind = bind_auto

    @staticmethod
    def write_log(log_f, message):
        print(message)
        log_f(f'--{datetime.now()}--\n{message}\n')

    def close_server(self):
        self.db_conn.close()
        self.write_log(logging.info, f'Закрытие сервера')

    def _db_init(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS clients'
            '(ip varchar(12) primary key,'
            'name varchar,'
            'password varchar)'
        )
        self.db_conn.commit()

    def start_server(self):
        logging.basicConfig(filename='server.log', level=logging.INFO)
        self._db_init()

        try:
            self.sock.bind(('', self.port))
            self.write_log(logging.info, f"Успешная связка с портом {self.port}")
        except OSError:
            if self.autobind:
                self.bind_auto()

        self.sock.listen(self.MAX_QUEUE)
        self.write_log(logging.info, f'Прослушивается порт {self.port}')

        threading.Thread(name='listening-sock', target=self.listen_sock).start()

    def bind_auto(self):
        for i in range(self.MIN_PORT, self.MAX_PORT):
            try:
                self.sock.bind(('', i))
                self.port = i
                self.write_log(logging.info, f"Успешная связка с портом {self.port}")
                break
            except OSError:
                pass
        else:
            msg = 'Остановка сервера: все порты заняты!'
            self.write_log(logging.error, msg)
            raise OSError(msg)

    def sign_up(self, client_sock):
        client_sock[0].send('Давайте вас зарегистрируем!\nУкажите имя: '.encode())
        name = client_sock[0].recv(1024).decode()
        client_sock[0].send('Укажите новый пароль: '.encode())
        password = client_sock[0].recv(1024).decode()
        os.mkdir(rf"C:\Users\Serg\Documents\MEGA\MEGAsync\PycharmProjects\UNIXOS\5_FTP_server\file_manager\{name}")

        sql = "INSERT INTO clients VALUES (?, ?, ?)"
        self.cursor.execute(sql, (client_sock[1][0], name, password))
        self.db_conn.commit()

        return name

    @staticmethod
    def sign_in(client_sock, name, password):
        while True:
            client_sock[0].send('Укажите пароль: '.encode())
            data = client_sock[0].recv(1024).decode()
            if data == password:
                return name
            else:
                client_sock[0].send('Неверный пароль! Попробуйте еще раз.'.encode())

    def identify_client(self, client_sock):
        sql = "SELECT * " \
              "FROM clients " \
              "WHERE ip = ?"
        client = self.cursor.execute(sql, (client_sock[1][0],)).fetchone()

        if client is None:
            name = self.sign_up(client_sock)
        else:
            name = self.sign_in(client_sock, client[1], client[2])

        return name

    def listen_sock(self):
        while True:
            client_sock = self.sock.accept()
            self.write_log(logging.info, f'Подключился пользователь: {client_sock[1]}')
            client_name = self.identify_client(client_sock)
            self.clients_conn[client_sock] = FileManager(client_name)
            threading.Thread(name=f'listening-{client_sock}',
                             target=self.listen_client_sock_data,
                             args=(client_sock, client_name)) \
                .start()
            # client_sock[0].send(f'{client_name} присоединился к нам! Добро пожаловать!'.encode())
            self.broadcast_msg(f' {client_sock[1]} - {client_name} присоединился к нам! Добро пожаловать!')

    def listen_client_sock_data(self, client_sock, name):
        while True:
            try:
                data = client_sock[0].recv(1024).decode()

                if data.startswith('/'):
                    file_manager = self.clients_conn[client_sock]
                    print(data)
                    data = file_manager.take_cmd(data[1:])
                    client_sock[0].send(data.encode())

                else:
                    data = f'{client_sock[1]} - {name}: {data}'
                    self.broadcast_msg(data)

            except ConnectionResetError as e:
                self.clients_conn.pop(client_sock)
                msg = f'Пользователь {client_sock[1]} - {name} покинул нас.'
                self.broadcast_msg(msg)
                self.write_log(logging.info, msg)

                print(e, client_sock[1])
                break

    def broadcast_msg(self, msg):
        for i in self.clients_conn:
            i[0].send(msg.encode())


if __name__ == '__main__':
    Server().start_server()
