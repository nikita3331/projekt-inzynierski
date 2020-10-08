from Point3D import Point
from MyDelaunay import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math
from random import random
from Point3D import Point
from timeit import default_timer as timer
import multiprocess 
import timeit


def count(items):
    xsyszs=[Point(0,0,0),Point(5,0,0),Point(5,5,0),Point(0,5,0),Point(0,0,5),Point(5,0,5),Point(5,5,5),Point(0,5,5),Point(5,5,6)]
    # xsyszs=[]
    # for itera in range(0,items):
    #     point=Point(random()*1000,random()*1000,random()*1000)
    #     xsyszs.append(point)
    comp=Delaunay(xsyszs)
    transformed,normalPoints=comp.computeVertices()
    comp.plotSelf()

if __name__ == '__main__':
    print('sredni czas ',timeit.timeit("count(1000)", setup="from __main__ import count",number=1)*1000/2,'ms')
    # count(100)