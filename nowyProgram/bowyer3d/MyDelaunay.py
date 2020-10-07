import numpy as np
import matplotlib.pyplot as plt
import math
from Point import Point
from Tetra import Tetrahedron

class Delaunay():
    #https://math.stackexchange.com/questions/2414640/circumsphere-of-a-tetrahedron
    #https://stackoverflow.com/questions/58116412/a-bowyer-watson-delaunay-triangulation-i-implemented-doesnt-remove-the-triangle
    def __init__(self,pointSet): #big A is point,small a is vertice
        self.pointSet=pointSet
        self.vertices=[]
        self.trianglePoints=[]
    def computeTrianglePoints(self):
        #https://www.youtube.com/watch?v=GctAunEuHt4&ab_channel=SCIco
        self.superTri=Triangle.createSuperTriangle(10000)
        triangulation=[] #empty triangle mesh data structure
        triangulation.append(self.superTri)  #add super-triangle to triangulation
        for p in self.pointSet: #for each point in set,add to triangulation
            badTriangles = []
            point=Point(p[0],p[1])
            for triangle in triangulation:
                if triangle.pointInBigCircle(point):
                    badTriangles.append(triangle)

            polygon = []
            for triangle in badTriangles:
                for edge in triangle.edges:
                    isShared = False
                    for other in badTriangles:
                        if triangle == other:
                            continue
                        for otherEdge in other.edges:
                            if Triangle.edgeIsEqual(edge,otherEdge):
                                isShared = True
                    if not isShared:
                        polygon.append(edge)
            for badTriangle in badTriangles:
                triangulation.remove(badTriangle)

            for edge in polygon:
                newTriangle = Triangle(edge[0],edge[1],point)
                triangulation.append(newTriangle)
        onSuper = lambda triangle : triangle.HasVertex(self.superTri.A) or triangle.HasVertex(self.superTri.B) or triangle.HasVertex(self.superTri.C)

        triangulation = [triangle for triangle in triangulation if not onSuper(triangle)]
        return triangulation
    def printAll(self,triangulation):
        print('=========================================================')            
        for idx,tri in enumerate(triangulation):
            print('index = ',idx)
            self.superTri.printSelf()
            tri.printSelf()
            print('================')
    def transformToIndexes(self):
        #adding indexes instead of values
        verticiesIndex=[]
        for triangle in self.trianglePoints:
            xs_new=[triangle.A.x,triangle.B.x,triangle.C.x]
            ys_new=[triangle.A.y,triangle.B.y,triangle.C.y]
            triTuple=[ (xs_new[0],ys_new[0]),(xs_new[1],ys_new[1]),(xs_new[2],ys_new[2])]
            newRow=[0,0,0]
            for idx,xy in enumerate(self.pointSet):
                for p in range(0,3):
                    if  triTuple[p][0]==xy[0] and triTuple[p][1]==xy[1]:
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
        self.trianglePoints=self.computeTrianglePoints()
        # self.cleaned=self.clearFromSuperTriangle()  #remove super triangle vertices and angles connected to them from full object
        self.transformed=self.transformToIndexes()  #transform values of points ,to indexes of them in main point set
        # self.withoutDuplicates=self.removeDuplicates()
        return self.transformed,self.trianglePoints
    def plotSelf(self):
        print(len(self.transformed))
        for vert in self.transformed:
            xs=[self.pointSet[index][0] for index in vert]
            ys=[self.pointSet[index][1] for index in vert]
            plt.fill(xs,ys)




