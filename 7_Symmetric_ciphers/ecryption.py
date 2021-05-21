from itertools import cycle
from random import randint
import math

char_len = 65536


def rnd_key(length: int) -> str:
    return "".join((chr(randint(0, char_len)) for _ in range(length)))


def cesar_encrypt(text: str, offset: int) -> str:
    return "".join(map(lambda c: chr((ord(c) + offset) % char_len), text))


def cesar_decrypt(text: str, offset: int) -> str:
    return "".join(map(lambda c: chr((ord(c) - offset) % char_len), text))


def cesar_hack(crypted: str) -> str:
    chars = {c: crypted.count(c) for c in set(crypted)}
    return cesar_encrypt(crypted, ord(' ') - ord(max(chars, key=chars.get)))


res = cesar_encrypt("Hello!", 2)
print("\nАлгоритм Цезаря\nЗакодированная строка:", res)
print("Декодирвоанная строка:", cesar_decrypt(res, 2))


def vigener_encrypt(text: str, key: str) -> str:
    return "".join(map(lambda k, c: chr((ord(c) + ord(k)) % char_len), cycle(key), text))


def vigener_decrypt(text: str, key: str) -> str:
    return "".join(map(lambda k, c: chr((ord(c) - ord(k)) % char_len), cycle(key), text))


res = vigener_encrypt('Hello, world!', "ab")
print("\nАлгоритм Вижинера\nЗакодированная строка:", res)

print("Декодированная строка:", vigener_decrypt(res, "ab"))


def vernom(text: str, key: str) -> str:
    return "".join(map(lambda k, c: chr(ord(c) ^ ord(k)), text, cycle(key)))


res = vernom('Hello, world!', "ab")
print("\nАлгоритм Вернама\nЗакодированная строка:", res)
print("Декодированная строка:", vernom(res, "ab"))


def otp(text: str) -> tuple[str, str]:
    key = rnd_key(len(text))
    return vernom(text, key), key


res, key = otp('Hello, world!')
print("\nАлгоритм OTP\nЗакодированная строка:", res)
print("Декодированная строка:", vernom(res, key))


def blockchain(text: str, func: callable, key, block_len: int = 5) -> tuple[str, str]:
    res = []
    v = rnd_key(block_len)
    blocks = [text[i:i+block_len] for i in range(0, len(text), block_len)]
    res.append(func(vernom(blocks.pop(0), v), key))
    while len(blocks) > 0:
        res.append(func(vernom(blocks.pop(0), res[-1]), key))
    return "".join(res), v


def blockchain_rev(text: str, v: str, de_func: callable, key, block_len: int = 5) -> str:
    res = []
    blocks = [text[i:i+block_len] for i in range(0, len(text), block_len)]
    while len(blocks) > 1:
        res.append(vernom(de_func(blocks.pop(-1), key), blocks[-1]))
    res.append(vernom(de_func(blocks.pop(-1), key), v))
    return "".join(reversed(res))


def feistel_cell(text: str, func: callable, K) -> str:
    sep = math.ceil(len(text) / 2)
    L = text[:sep]
    R = text[sep:]
    return R + vernom(func(L, K), R)


def feistel_cell_rev(text: str, de_func: callable, K) -> str:
    sep = math.ceil(len(text) / 2)
    L = text[:sep]
    R = text[sep:]
    return de_func(vernom(R, L), K) + L


def feistel_web(crypted: str, func: callable, K, iterations: int) -> str:
    for _ in range(iterations):
        crypted = feistel_cell(crypted, func, K)
    return crypted


def feistel_web_rev(crypted: str, de_func: callable, K, iterations: int) -> str:
    for _ in range(iterations):
        crypted = feistel_cell_rev(crypted, de_func, K)
    return crypted

