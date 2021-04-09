from threading import Thread
from multiprocessing import Process

i = 0


def print_to_file():
    f = open("m3.txt", 'a+')
    global i
    f.write(str(i))
    i += 1
    f.close()

# t1 = Thread(target=print_to_file)
# t2 = Thread(target=print_to_file)


p1 = Process(target=print_to_file)
p2 = Process(target=print_to_file)

# t1.start()
# t2.start()

p1.start()
p2.start()

