import numpy as np
import numba as nb
import time

def timeit(function):
    def wrapper():
        start = time.time()
        function()
        end = time.time()

        return end-start
    
    return wrapper

@timeit
def no_numba():
    a = np.random.rand(10000, 10000)
    b = np.random.rand(10000, 10000)
    c = np.zeros((10000, 10000))
    for i in range(10000):
        for j in range(10000):
            c[i][j] = a[i][j] + b[i][j]

@timeit
@nb.njit(fastmath=True)
def with_numba():
    a = np.random.rand(10000, 10000)
    b = np.random.rand(10000, 10000)
    c = np.zeros((10000, 10000))
    for i in range(10000):
        for j in range(10000):
            c[i][j] = a[i][j] + b[i][j]


print(with_numba())
print(no_numba())


