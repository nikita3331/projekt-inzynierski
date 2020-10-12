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


class Delaunay():
    #https://math.stackexchange.com/questions/2414640/circumsphere-of-a-tetrahedron
    #https://stackoverflow.com/questions/58116412/a-bowyer-watson-delaunay-triangulation-i-implemented-doesnt-remove-the-triangle
    def __init__(self,pointSet): #big A is point,small a is vertice
        self.pointSet=pointSet
        self.vertices=[]
        self.trianglePoints=[]
    def computeTrianglePoints(self):
        #https://www.youtube.com/watch?v=GctAunEuHt4&ab_channel=SCIco
        self.superTetra=Tetrahedron.createSuperTetra(10000)
        triangulation=[] #empty triangle mesh data structure
        triangulation.append(self.superTetra)  #add super-triangle to triangulation
        itera=0
        for idx,point in enumerate(self.pointSet): #for each point in set,add to triangulation
            if idx%100==0:
                print('Procent ukonczenia ',idx*100/len(self.pointSet),'%',flush=True)
            badTetra = []
            for tetra in triangulation:
                if tetra.pointInSphere(point):
                    badTetra.append(tetra)
                itera+=1
            for tetrahe in badTetra:
                myVert=tetrahe.vertecies
                allfaces=list(itertools.combinations(myVert, 3))
                buff=[]
                for face in allfaces:
                    buff.append(set(face))
                allfaces=buff
                sharedWithOtherFaces=[]
                for other in badTetra:
                    sharedFace=self.compareTetraFaces(myVert,other.vertecies)
                    if sharedFace!=[]:
                        allfaces.remove(set(sharedFace))
                for notSharedFace in allfaces:
                    listed=list(notSharedFace)
                    newTetra = Tetrahedron(listed[0],listed[1],listed[2],point)
                    triangulation.append(newTetra)
            for badTet in badTetra:
                itera+=1
                triangulation.remove(badTet)
                
        onSuper = lambda tetra : tetra.HasVertex(self.superTetra.A) or tetra.HasVertex(self.superTetra.B) or tetra.HasVertex(self.superTetra.C) or tetra.HasVertex(self.superTetra.D)
        print('liczba iteracji',itera)
        triangulation = [tetra for tetra in triangulation if not onSuper(tetra)]
        return triangulation
    def compareTetraFaces(self,vertA,vertB):
        dele=set (vertB ) - set(vertA)
        face=[]
        if dele!=set(vertB) and len(dele)==1:
            face=tuple(set(vertB)-dele)
        return face
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
        for tetra in self.tetraPoints:
            tetraTuple=[ tetra.A.toTuple(),tetra.B.toTuple(),tetra.C.toTuple(),tetra.D.toTuple()]
            newRow=[0,0,0,0]
            for idx,xyz in enumerate(self.pointSet):
                point=xyz.toTuple()
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
                xyz.append([self.pointSet[index].toArr()[0],self.pointSet[index].toArr()[1],self.pointSet[index].toArr()[2]])
            vertexComb= list(itertools.combinations(vert, 3))
            for p in vertexComb:
                faces.append(p)
            myFaceColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            colors.append(myFaceColor)
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
            p1=np.array(points[face[0]])
            p2=np.array(points[face[1]])
            p3=np.array(points[face[2]])
            N = np.cross(p2-p1, p3-p1)
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




