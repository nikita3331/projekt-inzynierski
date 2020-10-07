from Point3D import Point
from MyDelaunay import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math
from random import random
from Point3D import Point

xsys=[(3,3),(4,3),(5,2),(4,1),(3,1),(2,2)] #hex
# xsys=[(1,1),(0,2),(2,2),(1,3)] #square
#xsys=[(1,1),(0,2),(2,3),(1,3),(2,1)] #five

xsyszs=[]
for itera in range(0,40):
    point=Point(random()*100,random()*100,random()*100)
    xsyszs.append(point)
# xsyszs=[Point(0,0,0),Point(20,0,0),Point(0,0,30),Point(0,20,0)]

comp=Delaunay(xsyszs)
transformed,normalPoints=comp.computeVertices()
comp.plotSelf()
# xs=[point[0] for point in xsys]
# ys=[point[1] for point in xsys]

# plt.scatter(xs,ys)
# plt.show()