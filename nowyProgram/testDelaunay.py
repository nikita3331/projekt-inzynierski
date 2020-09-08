import numpy as np
import matplotlib.pyplot as plt
import math
from Point import Point
from Triangle import Triangle

class Delaunay():
    def __init__(self,pointSet): #big A is point,small a is vertice
        self.pointSet=pointSet
        self.vertices=[]
        self.trianglePoints=[]
    def computeTrianglePoints(self):
        #first we need to find triangle containing all points,for now super-triangle
        self.superTri=Triangle.createSuperTriangle(100)
        allTriangles=[]
        allTriangles.append(self.superTri)
        #https://www.youtube.com/watch?v=GctAunEuHt4&ab_channel=SCIco
        for p in self.pointSet:
            pickedPoint=Point(p[0],p[1])
            for triangleMain in allTriangles:
                if  triangleMain.pointInBigCircle(pickedPoint):
                    newtrilist=triangleMain.splitIntoTriangles(pickedPoint) 
                    allTriangles[:] = [tri for tri in allTriangles if tri!=triangleMain]
                    allTriangles+=newtrilist
        return allTriangles
    def clearFromSuperTriangle(self):
        vertices=[]
        verticiesIndex=[]
        #clear stage
        for triangle in self.trianglePoints:
            xs_new=[triangle.A.x,triangle.B.x,triangle.C.x]
            ys_new=[triangle.A.y,triangle.B.y,triangle.C.y]
            #we should better delete the ones containing super triangle
            if not (( (self.superTri.A.x in xs_new) or (self.superTri.B.x in xs_new) or (self.superTri.C.x in xs_new) ) and  ( (self.superTri.A.y in ys_new) or (self.superTri.B.y in ys_new) or (self.superTri.C.y in ys_new) )):
                vertices.append([ (xs_new[0],ys_new[0]),(xs_new[1],ys_new[1]),(xs_new[2],ys_new[2])])
        return vertices
    def transformToIndexes(self):
        #adding indexes instead of values
        verticiesIndex=[]
        for vert in self.cleaned:
            newRow=[0,0,0]
            for idx,xy in enumerate(self.pointSet):
                for p in range(0,3):
                    if  vert[p][0]==xy[0] and vert[p][1]==xy[1]:
                        newRow[p]=idx
            verticiesIndex.append(newRow)
        return verticiesIndex
    def removeDuplicates(self):
        #remove duplicate items from array of triangles ,[1,2,3]=[3,2,1]=duplicate [1,2,3]=[1,2,3]=duplicate
        filtered=[]
        copied=self.transformed.copy()
        for pickedTriangle in copied:
            for index,triangle in enumerate(copied):
                if triangle!=pickedTriangle:
                    if  pickedTriangle[0] in triangle and pickedTriangle[1] in triangle and pickedTriangle[2] in triangle:  #remove duplicated point but in other order
                        copied[:] = [tri for tri in copied if tri!=triangle]
                else:
                    numberOfAccurances=copied.count(triangle)
                    if numberOfAccurances>1:
                        copied[:] = [tri for idx,tri in enumerate(copied) if idx!=index]
        return copied

    def computeVertices(self):
        self.trianglePoints=self.computeTrianglePoints()    #compute all of the triangle points
        self.cleaned=self.clearFromSuperTriangle()  #remove super triangle vertices and angles connected to them from full object
        self.transformed=self.transformToIndexes()  #transform values of points ,to indexes of them in main point set
        self.withoutDuplicates=self.removeDuplicates()
        return self.transformed,self.withoutDuplicates
    def plotSelf(self):
        for vert in self.withoutDuplicates:
            xs=[self.pointSet[index][0] for index in vert]
            ys=[self.pointSet[index][1] for index in vert]
            plt.fill(xs,ys)

xsys=[(3,3),(4,3),(5,2),(4,1),(3,1),(2,2)] #hex
xsys=[(1,1),(0,2),(2,2),(1,3)] #square
xsys=[(1,1),(0,2),(2,3),(1,3),(2,1)] #five



comp=Delaunay(xsys)
transformed,withoutDuplicates=comp.computeVertices()
print(len(transformed))
print(len(withoutDuplicates))
comp.plotSelf()
xs=[point[0] for point in xsys]
ys=[point[1] for point in xsys]

plt.scatter(xs,ys)




plt.show()


