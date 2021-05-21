import socket
from config import *
import os


class Request:
    def __init__(
            self,
            method: str = "GET",
            url: str = "/",
            protocol: str = "HTTP/1.1",
            headers: dict = None,
            body: str = ""
    ):
        self.headers = headers
        if self.headers is None:
            self.headers = dict()
        self.method = method
        self.url = url
        self.protocol = protocol
        self.body = body

    @staticmethod
    def parse(request: str):
        ans = request.split(SEP)
        method, url, protocol = ans.pop(0).split()
        body_sep = ans.index("")
        headers = dict()
        for row in ans[:body_sep]:
            k, v = row.split(": ", 1)
            headers.update({k: v})
        body = SEP.join(ans[body_sep + 1:])
        return Request(method, url, protocol, headers, body)


class Response:
    def __init__(
            self,
            protocol: str = "HTTP/1.1",
            code: int = 200,
            status: str = "OK",
            headers: dict = None,
            body: str = ""
    ):
        self.protocol = protocol
        self.code = code
        self.status = status
        self.headers = headers
        if self.headers is None:
            self.headers = dict()
        self.body = body

    def concatenating(self) -> str:
        ans = [f'{self.protocol} {self.code} {self.status}',
               SEP.join(map(lambda k, v: f'{k}: {v}', self.headers.keys(), self.headers.values())), SEP, self.body]
        return SEP.join(ans)


def read_file(path: str) -> str:
    if path == "" or path == "/":
        path = "/index.html"

    path = WORK_DIRECTORY + path

    if os.path.isfile(path):
        with open(path, 'r') as f:
            return "".join((f"{line}\n" for line in f))
    else:
        with open(WORK_DIRECTORY + "/404.html", 'r') as f:
            return "".join((f"{line}\n" for line in f))


def start_server():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(MAX_REQ_SIZE)
        msg = data.decode(ENC)
        req = Request.parse(msg)

        code = 200
        status = 'OK'

        body = read_file(req.url)
        print(body)
        if body == "":
            code = 404
            status = 'NOT_FOUND'
        response = Response(
            code=code,
            status=status,
            headers={"Content-type": f"text/html;charset={ENC}"},
            body=body
        )
        conn.send(response.concatenating().encode(ENC))
        conn.close()


if __name__ == '__main__':
    start_server()
