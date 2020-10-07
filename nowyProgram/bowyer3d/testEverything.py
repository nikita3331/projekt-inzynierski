from Point3D import Point
from MyDelaunay import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math
from random import random
from Point3D import Point
from timeit import default_timer as timer
import multiprocess 


def count(items):
    xsyszs=[]
    for itera in range(0,items):
        point=Point(random()*100,random()*100,random()*100)
        xsyszs.append(point)
    # xsyszs=[Point(0,0,0),Point(20,0,0),Point(0,0,30),Point(0,20,0)]
    start = timer()
    comp=Delaunay(xsyszs)
    transformed,normalPoints=comp.computeVertices()
    # comp.plotSelf()
    end = timer()
    times.append(end-start)
    xaxis.append(items)
    
    print('koniec ',items)
    return (times,xaxis)



def initializer():
    global times
    times = []
    global xaxis
    xaxis = []
    
if __name__ == '__main__':
    

    pool = multiprocess.Pool(1,initializer,())
    time=pool.map(count, range(4,25))
    pool.close()
    time.sort(key=lambda x:len(x),reverse=True)
    myTimes=time[0][0]
    myInd=time[0][1]

    filed=[]
    for tim,ind in zip(myTimes,myInd):
        filed.append((tim,ind))
    filed.sort(key=lambda x:x[1],reverse=False)
    
    
    plt.plot(filed[:][1],filed[:][0])
    plt.show()
    print('koniec')