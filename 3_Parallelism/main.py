from multiprocessing import Process, Pool
from threading import Thread
from time import time
from random import randint


def element(index, a, b):
    global res
    i, j = index
    s = 0
    n = len(a)
    for k in range(n):
        s += a[i][k] * b[k][j]
    # file.write(f'{s} ')
    # if j == n - 1:
    #     file.write('\n')
    #
    # file.close()


# def read_matrix(source):
#     matrix = []
#     with open(source, 'r') as f:
#         for i in f:
#             matrix.append(list(map(lambda x: float(x), i.strip().split())))
#
#     return matrix


def create_thread_pool(func, length, index, a, b):
    i, j = index
    while True:
        if j % len(a) == 0 and j != 0:
            j = 0
            i += 1

        # file = open('result.txt', 'a')
        Thread(target=func, args=((i, j), a, b)).start()

        j += 1
        length -= 1

        if not length:
            break


def start(max_len_pool=1):
    # a = read_matrix('m1.txt')
    # b = read_matrix('m2.txt')
    global n
    print(n)

    a = [[randint(-100, 100) for _ in range(n)] for _ in range(n)]
    b = [[randint(-100, 100) for _ in range(n)] for _ in range(n)]

    n = len(a)
    threads = n * n
    i, j = 0, 0

    h = threads // max_len_pool
    o = threads % max_len_pool

    for _ in range(max_len_pool):
        k = 0
        if o:
            k = 1
            o -= 1

        y = h + k

        Process(target=create_thread_pool, args=(element, y, (i, j), a, b)).start()

        i += y // len(a)
        j += y % len(a)

        if j > len(a):
            j = j % len(a)
            i += 1


if __name__ == '__main__':
    t = time()
    n = 1000
    res = [[0 for _ in range(n)] for _ in range(n)]
    max_len_pool = 4
    start(max_len_pool)
    print(time() - t)
    print(res)
