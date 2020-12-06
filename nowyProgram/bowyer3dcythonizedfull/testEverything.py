from MyDelaunay import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from timeit import default_timer as timer
import multiprocess 
import timeit
import trimesh
import open3d as o3d
from mpl_toolkits.mplot3d import axes3d, Axes3D


def generatePoints(leng):
    xsyszs=[]
    xs=np.load('testingxs1.npy')
    ys=np.load('testingys1.npy')
    zs=np.load('testingzs1.npy')
    itera=3
    # for idx in range(0,len(xs)):
    #     if idx%2==0:
    #         point=(xs[idx],ys[idx],zs[idx],itera) #x,y,z+index
    #     else:
    #         point=(xs[-idx],ys[-idx],zs[-idx],itera) #x,y,z+index
    #     # print(point)
    #     xsyszs.append(point)
    #     itera+=1
        
    # print(len(xsyszs))
    xsyszs=[]
    for i in range(0,leng):
        point=(random.randrange(-10,10),random.randrange(-10,10),random.randrange(-10,10),i) #x,y,z+index
        xsyszs.append(point)
        # print(point)
    # point=(100,200,300,leng) #x,y,z+index
    # xsyszs.append(point)
    # point=(100,200,400,leng+1) #x,y,z+index
    # xsyszs.append(point)
    # point=(50,200,400,leng+2) #x,y,z+index
    # xsyszs.append(point)
        
    print(len(xsyszs))
    return xsyszs
def count(pts):
    comp=Delaunay(pts)
    transformed,normalPoints=comp.computeVertices()
    output=comp.plotSelf() #for showing tetra


if __name__ == '__main__':
    pts=generatePoints(1000)
    print('sredni czas nowego',timeit.timeit("count(pts)", setup="from __main__ import count,pts",number=1)*1000/1,'ms')
    # count(100)