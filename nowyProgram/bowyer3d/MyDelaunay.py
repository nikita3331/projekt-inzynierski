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
        for point in self.pointSet: #for each point in set,add to triangulation
            badTetra = []
            for tetra in triangulation:
                if tetra.pointInSphere(point):
                    badTetra.append(tetra)
                itera+=1

            polygon = []
            for tetrahe in badTetra:
                for face in tetrahe.faces:
                    isShared = False
                    for other in badTetra:
                        if tetrahe == other:
                            continue
                        for otherFace in other.faces:
                            itera+=1
                            if Tetrahedron.faceIsEqual(face,otherFace):
                                isShared = True
                    if not isShared:
                        polygon.append(face)
            for badTet in badTetra:
                itera+=1
                triangulation.remove(badTet)

            for face in polygon:
                itera+=1
                newTetra = Tetrahedron(face[0],face[1],face[2],point)
                triangulation.append(newTetra)
        onSuper = lambda tetra : tetra.HasVertex(self.superTetra.A) or tetra.HasVertex(self.superTetra.B) or tetra.HasVertex(self.superTetra.C) or tetra.HasVertex(self.superTetra.D)
        print('liczba iteracji',itera)
        triangulation = [tetra for tetra in triangulation if not onSuper(tetra)]
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
        for tetra in self.tetraPoints:
            xs_new=[tetra.A.x,tetra.B.x,tetra.C.x,tetra.D.x]
            ys_new=[tetra.A.y,tetra.B.y,tetra.C.y,tetra.D.y]
            zs_new=[tetra.A.z,tetra.B.z,tetra.C.z,tetra.D.z]
            tetraTuple=[ (xs_new[0],ys_new[0],zs_new[0]),(xs_new[1],ys_new[1],zs_new[1]),(xs_new[2],ys_new[2],zs_new[2]),(xs_new[3],ys_new[3],zs_new[3])]
            newRow=[0,0,0,0]
            for idx,xyz in enumerate(self.pointSet):
                point=xyz.toArr()
                for p in range(0,4):
                    if  tetraTuple[p][0]==point[0] and tetraTuple[p][1]==point[1] and tetraTuple[p][2]==point[2]:
                        newRow[p]=idx
            verticiesIndex.append(newRow)
        return verticiesIndex


    def computeVertices(self):
        self.tetraPoints=self.computeTrianglePoints()
        self.transformed=self.transformToIndexes()  #transform values of points ,to indexes of them in main point set
        return self.transformed,self.tetraPoints
    def plotSelf(self):
        fullPoints=[]
        xyz=[]
        
        for vert in self.transformed:
            for index in vert:
                xyz.append([self.pointSet[index].toArr()[0],self.pointSet[index].toArr()[1],self.pointSet[index].toArr()[2]])
        faces=[]
        colors=[]
        for tetra in self.transformed:
            vertexComb= list(itertools.combinations(tetra, 3))
            for p in vertexComb:
                faces.append(p)
            myFaceColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            colors.append(myFaceColor)
            colors.append(myFaceColor)
            colors.append(myFaceColor)
            colors.append(myFaceColor)
        tri_mesh = trimesh.Trimesh(vertices=xyz,faces=faces,vertex_colors=colors) 
        tri_mesh.export('test.ply')
        pcd_load = o3d.io.read_triangle_mesh("test.ply")
        o3d.visualization.draw_geometries([pcd_load],window_name='delaunay')




