import numpy as np
from Point3D import Point
import collections
import itertools
import timeit
from operator import itemgetter
import time
from multiprocessing import Process, Manager,Pool
import math



def myfunc(iterator):
    total=0
    for i in range(0,1000):
        for j in range(0,1000):
            total+=i*j
    return total

if __name__ == '__main__':






    startTime=time.time()
    pool = Pool()

    vals=pool.starmap(myfunc, ((i,) for i in range(0, 100)))
    pool.close()
    print(vals)
    endTime=time.time()
    print('czas pierwszegop',endTime-startTime)
    lista=[]
    startTime=time.time()
    for i in range(0,100):
        total=0
        for j in range(0,1000):
            for k in range(0,1000):
                total+=j*k
        lista.append(total)
    
    endTime=time.time()
    
    print('czas drguiego',endTime-startTime)
    returned=np.array(lista)-np.array(vals)
    print(returned)






