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


def generatePoints(leng):
    xsyszs=[]
    for itera in range(0,leng):
        point=(random()*1000,random()*1000,random()*1000)
        xsyszs.append(point)
    return xsyszs
def count(pts):
    #xsyszs=[Point(0,0,0),Point(5,0,0),Point(5,5,0),Point(0,5,0),Point(0,0,5),Point(5,0,5),Point(5,5,5),Point(0,5,5),Point(5,5,6),Point(10,11,12)]

    comp=Delaunay(pts)
    transformed,normalPoints=comp.computeVertices()
    comp.plotSelf() #for showing tetra

if __name__ == '__main__':
    pts=generatePoints(1000)
    print('sredni czas nowego',timeit.timeit("count(pts)", setup="from __main__ import count,pts",number=1)*1000/1,'ms')
    # count(100)