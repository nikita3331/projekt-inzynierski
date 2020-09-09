from Point import Point
from MyDelaunay import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math
xsys=[(3,3),(4,3),(5,2),(4,1),(3,1),(2,2)] #hex
xsys=[(1,1),(0,2),(2,2),(1,3)] #square
xsys=[(1,1),(0,2),(2,3),(1,3),(2,1)] #five



comp=Delaunay(xsys)
transformed,withoutDuplicates=comp.computeVertices()
print(transformed)
print(withoutDuplicates)
print(comp.superTri.printSelf())
comp.plotSelf()
xs=[point[0] for point in xsys]
ys=[point[1] for point in xsys]

plt.scatter(xs,ys)
plt.show()