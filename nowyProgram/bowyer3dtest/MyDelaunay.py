import numpy as np
import matplotlib.pyplot as plt
import math
from Point3D import Point
from Tetra import Tetrahedron
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import axes3d, Axes3D
import open3d as o3d
import trimesh
import itertools
import random
import collections
import time
from multiprocessing import Process, Manager


class Delaunay():
    #https://math.stackexchange.com/questions/2414640/circumsphere-of-a-tetrahedron
    def __init__(self,pointSet):
        self.pointSet=pointSet
        self.vertices=[]
        self.trianglePoints=[]
    def removeSharedFace(self,myVert,otherVert,allFaces):
        if len(allFaces)>0:
            sharedFace=self.compareTetraFaces(myVert,otherVert)
            if len(sharedFace)==3:
                allFaces.remove(sharedFace)
        return allFaces
    def removeTouchingTetra(self,tetrahe,badTetra,triangulation,point):
        myVert=tetrahe.vertecies
        allfaces=[{myVert[0],myVert[1],myVert[2]},{myVert[0],myVert[1],myVert[3]},{myVert[3],myVert[1],myVert[2]},{myVert[0],myVert[3],myVert[2]}]
        #----
        #--this takes 48% of time
        sharedWithOtherFaces=[]
        for other in badTetra: #check if our tetrahedra hes 3 same vertices ,so has the same face
            allfaces=self.removeSharedFace(myVert,other.vertecies,allfaces)               
        #----
        #---this takes 10% of time
        for notSharedFace in allfaces:
            first, second,third = notSharedFace
            triangulation.append(Tetrahedron(first,second,third,point))
        #---
        triangulation.remove(tetrahe)
    def computeTrianglePoints(self):
        self.superTetra=Tetrahedron.createSuperTetra(10000) #first create super tetra where are all points
        triangulation=[] #all triangles go here
        triangulation.append(self.superTetra)  #add first super tri,remove it at the end
        itera=0
        totalStartTime=time.time()
        firstTime=0
        secondTime=0
        for idx,point in enumerate(self.pointSet):
            if idx%100==0:
                print('Procent ukonczenia ',idx*100/len(self.pointSet),'%',flush=True)
            badTetra = []
            firstT=time.time()
            for tetra in triangulation: # lets check if point is in sphere of any tetrahedra
                if tetra.pointInSphere(point):
                # if tetra.isInSphere(point):
                    badTetra.append(tetra)
                itera+=1
            firstET=time.time()
            firstTime+=(firstET-firstT)
            firstT=time.time()
            for tetrahe in badTetra: #here we check if our tetrahedra touches with other ones
                self.removeTouchingTetra(tetrahe,badTetra,triangulation,point) #prepared for multiprocess
            firstET=time.time()
            secondTime+=firstET-firstT
        totalEndTime=time.time()
        totTime=totalEndTime-totalStartTime
        print('totaj time',totTime,'first time percentage',firstTime*100/totTime,'%',"second time ",secondTime*100/totTime,'%')

                
                
        # onSuper = lambda tetra : len({*tetra.vertecies}.intersection({*self.superTetra.vertecies}))>0
        onSuper = lambda tetra : len(np.intersect1d(tetra.vertecies, self.superTetra.vertecies))>2

        print('liczba iteracji',itera)
        triangulation = [tetra for tetra in triangulation if not onSuper(tetra)]
        return triangulation
    def compareTetraFaces(self,vertA,vertB):
        face=set(vertB).intersection(set(vertA)) #how many verticies are the same
        return face

    def transformToIndexes(self):
        #adding indexes instead of values
        verticiesIndex=[]
        for tetra in self.tetraPoints:
            tetraTuple=[ tetra.A,tetra.B,tetra.C,tetra.D]
            newRow=[0,0,0,0]
            for idx,xyz in enumerate(self.pointSet):
                point=xyz
                for indx,tup in enumerate(tetraTuple):
                    if  tup==point:
                        newRow[indx]=idx
            verticiesIndex.append(newRow)
        return verticiesIndex

    def computerVertexCoordsFacesColors(self):
        xyz=[]
        faces=[]
        colors=[]
        for vert in self.transformed:
            for index in vert:
                myPt=self.pointSet[index]
                xyz.append([myPt[0],myPt[1],myPt[2]])
            vertexComb= list(itertools.combinations(vert, 3))
            for p in vertexComb: #adding faces of tetrahedra
                faces.append(p)
            myFaceColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            colors.append(myFaceColor)#same color for each face of tetra
            colors.append(myFaceColor)
            colors.append(myFaceColor)
            colors.append(myFaceColor)

        return xyz,faces,colors
    def computeVertices(self):
        self.tetraPoints=self.computeTrianglePoints()
        self.transformed=self.transformToIndexes()  #transform values of points ,to indexes of them in main point set
        return self.transformed,self.tetraPoints
    def computeNormals(self,faces,points):
        normals=[]
        for face in faces:
            p1=points[face[0]]
            p2=points[face[1]]
            p3=points[face[2]]
            N = np.cross(np.subtract(p2,p1),np.subtract(p3,p1))
            normals.append(N)
        return normals
    def plotSelf(self):
        fullPoints=[]
        xyz,faces,colors=self.computerVertexCoordsFacesColors()     
        normals=self.computeNormals(faces,xyz)  
        tri_mesh = trimesh.Trimesh(vertices=xyz,faces=faces,vertex_normals=normals,vertex_colors=colors) 
        tri_mesh.export('test.ply')
        pcd_load = o3d.io.read_triangle_mesh("test.ply")
        o3d.visualization.draw_geometries([pcd_load],window_name='delaunay')




