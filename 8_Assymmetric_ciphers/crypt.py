import random
from itertools import cycle


def create_param(start=10**4, end=10**6) -> int:
    return random.randint(start, end)


def write_key(path: str, params: list):
    with open(path, 'w') as f:
        for p in params:
            f.write(f'{p}\n')


def read_key(path: str) -> str:
    ans = []
    with open(path, 'r') as f:
        for line in f:
            ans.append(line)
    return "".join(ans)


def create_sym_key(ab: int, AB: int, p: int) -> int:
    return round(AB ** ab % p)


def cipher(key: str, text: str) -> str:
    return "".join(map(lambda k, c: chr((ord(c) ^ ord(k)) % 65536), cycle(key), text))
