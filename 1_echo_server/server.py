import socket
import logging
from datetime import datetime
import sqlite3


class User:
    def __init__(self, ip, name, password):
        self._ip = ip
        self._name = name
        self._password = password


conn_db = sqlite3.connect("echo_server.db")
cursor = conn_db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS clients("
               "ip VARCHAR PRIMARY KEY,"
               "name VARCHAR NOT NULL,"
               "pwd_hash VARCHAR)")

logging.basicConfig(filename='server.log', level=logging.INFO)

sock = socket.socket()
port = 9090
max_port = 10000


def close_server():
    conn_db.close()
    exit()


def change_name(ip, name):
    sql = "UPDATE clients SET name =? WHERE ip = ?"
    cursor.execute(sql, (name, ip))
    conn_db.commit()

    return f"Имя успешно измененно на {name}!"


def write_log(log_f, message):
    print(message)
    log_f(f'--{datetime.now()}--\n{message}\n')


def get_data():
    data = None
    try:
        data = conn.recv(1024).decode()
    except (ConnectionResetError, KeyboardInterrupt) as e:
        write_log(logging.error, f"Stop program: lost connection from client({e})")
        # close_server()
    return data


def _is_null(obj, name:str):
    if obj is None or not obj:
        conn.send(f"Неккортный ввод: {name}".encode())
        return True
    return False


def registration(ip):
    # поток
    # вынести в функцию
    name: str = ''
    password: str = ''

    while True:
        conn.send("Создайте имя: ".encode())
        name = get_data()
        if name == 'exit':
            exit()
        if _is_null(name, "имя"):
            continue

        conn.send(f"Создайте пароль для {name}: ".encode())
        password = get_data()
        if password == 'exit':
            exit()
        if _is_null(password, "пароль"):
            continue

        break



    sql = "INSERT INTO clients VALUES(?,?,?)"
    cursor.execute(sql, (addr[0], name, password))
    conn_db.commit()





def authentication(ip):

    sql = "SELECT name " \
          "FROM clients " \
          "WHERE ip = ?"

    client = cursor.execute(sql, (ip,)).fetchone()

    if not client:
        conn.send("Создайте имя: ".encode())
        name = get_data()
        conn.send(f"Создайте пароль для {name}: ".encode())
        password = get_data()

        # сделать проверку на валидность пароля и имя
        if name is not None and password is not None:

            sql = "INSERT INTO clients VALUES(?,?,?)"
            cursor.execute(sql, (addr[0], name, password))
            conn_db.commit()
        else:
            conn.send("Некорректное имя!".encode())
            write_log(logging.warning, "Некорректное имя!")

            return None
    else:
        name = client[0]

    conn.send(f"Идентификация прошла успешно, {name}!".encode())

    return name


# Попытка связать порт
while True:
    if port > max_port:
        write_log(logging.error, "Остановка программы: не найдены свободные порты!")

    try:
        sock.bind(('', port))
        write_log(logging.info, f"Успешная связка с портом {port}")
        break
    except OSError:
        port += 1

while True:
    write_log(logging.info, f"Слушаем порт {port}")
    sock.listen(max_port)

    try:
        conn, addr = sock.accept()
        ip = addr[0]
        number = addr[1]
    except KeyboardInterrupt as k:
        write_log(logging.error, f"Stop program: \n{k}")
        close_server()

    client_name = authentication(addr[0])

    if client_name is None:
        continue

    write_log(logging.info, f'Соединение установлено: ({ip}, {number}, {client_name})')

    while True:
        data = get_data()

        print(data)

        if data == "/change_name":
            conn.send("Ввведите имя:".encode())
            new_name = get_data()

            msg = f"({ip}, {number}, {client_name}): {change_name(ip, new_name)}"

            client_name = new_name
            conn.send(msg.encode())
            write_log(logging.info, msg)

            continue

        if data == '':
            break

        conn.send(data.upper().encode())
