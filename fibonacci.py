import numpy
import time

O = numpy.matrix([[1, 1], [1, 0]])
I = numpy.matrix([[1, 0], [0, 1]])

def iterfibo(n):
    ret = O * O
    for i in range(n - 2):
        ret *= O
    return ret[0, 0]

def fibo(n, M = O):
    if n == 1:
        return M
    return fibo(n - 1, M * O)

while True:
    nbr = int(input("Enter a number: "))
    if nbr == -1:
        break
    ts = time.time()
    fibonumber = iterfibo(nbr - 1)
    ts = time.time() - ts
    print("IterFibo(%d)=%d, time %.6f" %(nbr, fibonumber, ts))
    ts = time.time()
    fibonumber = fibo(nbr - 1)[0, 0]
    ts = time.time() - ts
    print("Fibo(%d)=%d, time %.6f" %(nbr, fibonumber, ts))
