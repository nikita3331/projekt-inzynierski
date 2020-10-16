import numpy as np
from Point3D import Point
import collections
import itertools
import timeit
from operator import itemgetter
import time
from multiprocessing import Process, Manager,Pool
import math



def myfunc(lista,iterator):
    total=0
    for i in range(0,1000):
        for j in range(0,1000):
            total+=i*j
    lista.append(total)

if __name__ == '__main__':
    manager = Manager()

    l = manager.list()
    processes=[]





    startTime=time.time()
    pool = Pool(processes=5)

    pool.starmap(myfunc, ((l, i) for i in range(0, 100)))
    pool.close()

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
    returned=np.array(lista)-np.array(l)
    print(returned)






