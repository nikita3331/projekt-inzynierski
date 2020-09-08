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
    # def computeTrianglePoints(self):
    #     #first we need to find triangle containing all points,for now super-triangle
    #     self.superTri=Triangle.createSuperTriangle(100)
    #     allTriangles=[]
    #     allTriangles.append(self.superTri)
    #     #https://www.youtube.com/watch?v=GctAunEuHt4&ab_channel=SCIco
    #     for p in self.pointSet:
    #         pickedPoint=Point(p[0],p[1])
    #         for triangleMain in allTriangles:
    #             if  triangleMain.pointInBigCircle(pickedPoint):
    #                 newtrilist=triangleMain.splitIntoTriangles(pickedPoint) 
    #                 allTriangles[:] = [tri for tri in allTriangles if tri!=triangleMain]
    #                 allTriangles+=newtrilist
    #     return allTriangles
    def computeTrianglePoints(self):
        #https://www.youtube.com/watch?v=GctAunEuHt4&ab_channel=SCIco
        self.superTri=Triangle.createSuperTriangle(100)
        triangulation=[] #empty triangle mesh data structure
        triangulation.append(self.superTri)  #add super-triangle to triangulation
        for p in self.pointSet: #for each point in set,add to triangulation
            badTriangles=[] #empty set or triangles
            pickedPoint=Point(p[0],p[1])    #create point object
            for triangle in triangulation:  #lets check which are not valid anymore
                if  triangle.pointInBigCircle(pickedPoint):
                    badTriangles.append(triangle)
            polygon=[]  #emty set for polygon

            badTriangleEdges=[] #add edges of all triangles for easier filtering
            for triangle in badTriangles:
                badTriangleEdges+=triangle.edges

            for badTri in badTriangles:  #find the boundary of the polygonal hole
                for edge in badTri.edges: 
                    if badTriangleEdges.count(edge)<3: #---before was 2 edge not shared by any other triangle,do something with it !!!!
                        polygon.append(edge)


            # for triangle in badTriangles: # remove them from the data structure
            #     triangulation[:] = [tri for tri in triangulation if tri!=triangle]
            
            for edge in polygon: # re-triangulate the polygonal hole
                newTri =Triangle(edge[0],edge[1],pickedPoint) #form a triangle from edge to point
                triangulation.append(newTri) #add newTri to triangulation
        for idx,triangle in enumerate(triangulation): # done inserting points, now clean up
            superVertexes=[self.superTri.A,self.superTri.B,self.superTri.C]
            if  triangle.A in superVertexes or triangle.B in superVertexes or triangle.C in superVertexes:  #if containts vertex from SUPER
                triangulation[:] = [tri for index,tri in enumerate(triangulation) if index!=idx]
        
        print('=========================================================')            
        for idx,tri in enumerate(triangulation):
            print('index = ',idx)
            self.superTri.printSelf()
            tri.printSelf()
            print('================')

        return triangulation
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
        for vert in self.transformed:
            xs=[self.pointSet[index][0] for index in vert]
            ys=[self.pointSet[index][1] for index in vert]
            plt.fill(xs,ys)




