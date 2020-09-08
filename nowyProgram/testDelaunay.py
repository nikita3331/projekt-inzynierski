import numpy as np
import matplotlib.pyplot as plt
import math
from Point import Point
from Triangle import Triangle



xsys=[(3,3),(4,3),(5,2),(4,1),(3,1),(2,2)] #hex
# xsys=[(1,1),(2,1),(1,2),(2,2)] #square


#first we need to find triangle containing all points,for now super-triangle
superTri=Triangle.createSuperTriangle(100)
allTriangles=[]
allTriangles.append(superTri)

#https://www.youtube.com/watch?v=GctAunEuHt4&ab_channel=SCIco
for p in xsys:
    pickedPoint=Point(p[0],p[1])
    for triangleMain in allTriangles:
        if  triangleMain.pointInBigCircle(pickedPoint):
            newtrilist=triangleMain.splitIntoTriangles(pickedPoint) 
            allTriangles[:] = [tri for tri in allTriangles if tri!=triangleMain]
            allTriangles+=newtrilist


vertices=[]
verticiesIndex=[]

#clear stage
for triangle in allTriangles:
    xs_new=[triangle.A.x,triangle.B.x,triangle.C.x]
    ys_new=[triangle.A.y,triangle.B.y,triangle.C.y]
    #we should better delete the ones containing super triangle
    if not (( (superTri.A.x in xs_new) or (superTri.B.x in xs_new) or (superTri.C.x in xs_new) ) and  ( (superTri.A.y in ys_new) or (superTri.B.y in ys_new) or (superTri.C.y in ys_new) )):
        vertices.append([ (xs_new[0],ys_new[0]),(xs_new[1],ys_new[1]),(xs_new[2],ys_new[2])])
        plt.fill(xs_new,ys_new)

xs=[point[0] for point in xsys]
ys=[point[1] for point in xsys]

print(xs)
plt.scatter(xs,ys)

#adding indexes instead of values
for vert in vertices:
    newRow=[0,0,0]
    for idx,xy in enumerate(xsys):
        for p in range(0,3):
            if  vert[p][0]==xy[0] and vert[p][1]==xy[1]:
                newRow[p]=idx
    verticiesIndex.append(newRow)

plt.show()


