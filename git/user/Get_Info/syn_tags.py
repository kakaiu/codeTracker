import multiprocessing
import time


def f(x):
    for i in range(x):
        for j in range(i):
            print(j)
    # time.sleep(2)
    print(x)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=5)
    pool.map(f, range(10))