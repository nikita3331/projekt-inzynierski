from MyDelaunay import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math
from random import random
from timeit import default_timer as timer
import multiprocess 
import timeit
import trimesh
import open3d as o3d



def generatePoints(leng):
    xsyszs=[]
    for itera in range(0,leng):
        point=(random()*1000,random()*1000,random()*1000,itera) #x,y,z+index
        xsyszs.append(point)
    return xsyszs
def count(pts):
    #xsyszs=[Point(0,0,0),Point(5,0,0),Point(5,5,0),Point(0,5,0),Point(0,0,5),Point(5,0,5),Point(5,5,5),Point(0,5,5),Point(5,5,6),Point(10,11,12)]

    comp=Delaunay(pts)
    transformed,normalPoints=comp.computeVertices()
    output=comp.plotSelf() #for showing tetra
    # tri_mesh = trimesh.Trimesh(vertices=output[0],faces=output[1],vertex_colors=output[2]) 
    # tri_mesh.export('test.ply')
    # pcd_load = o3d.io.read_triangle_mesh("test.ply")
    # o3d.visualization.draw_geometries([pcd_load],window_name='delaunay')


if __name__ == '__main__':
    pts=generatePoints(1000)
    print('sredni czas nowego',timeit.timeit("count(pts)", setup="from __main__ import count,pts",number=1)*1000/1,'ms')
    # count(100)