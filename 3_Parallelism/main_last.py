from multiprocessing import Pool
from random import randint
from time import time


def element(index, a, b):
    i, j = index
    s = 0
    n = len(a)
    for k in range(n):
        s += a[i][k] * b[k][j]

    return s


if __name__ == "__main__":
    # a = [[1, 4],
    #      [2, 5]]
    # b = [[3, 1],
    #      [3, 2]]
    n = 100
    a = [[randint(-100, 100) for _ in range(n)] for _ in range(n)]
    b = [[randint(-100, 100) for _ in range(n)] for _ in range(n)]

    t = time()

    def gen():
        for i in range(n):
            for j in range(n):
                yield (i, j), a, b

    pool = Pool(processes=4)
    print(
        pool.starmap(element, gen())
    )

    print(time() - t)



