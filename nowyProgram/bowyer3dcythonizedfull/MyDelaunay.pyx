cimport numpy as np
import numpy as np
from libc.math cimport sqrt,pow
from Point3D import Point
cimport Tetra
import random
import time
from contextlib import suppress

cdef class Delaunay():
    #https://math.stackexchange.com/questions/2414640/circumsphere-of-a-tetrahedron
    cdef public:
        cdef list pointSet
        cdef list vertices
        cdef list trianglePoints
        cdef list tetraPoints
        cdef list transformed
        cdef set lastRemoved
        cdef set lastLastRemoved
        cdef set lastLastLastRemoved
        cdef set lastLastLastLastRemoved
        
        cdef Tetra.Tetrahedron superTetra
    def __init__(self,list pointSet):
        self.pointSet=pointSet
        self.vertices=[]
        self.trianglePoints=[]
        self.superTetra=self.createSuperTetra(100) #first create super tetra where are all points

    cdef list removeSharedFace(self,list myVert,list otherVert,list allFaces):
        cdef set sharedFace
        if len(allFaces)>0:
            sharedFace=self.compareTetraFaces(myVert,otherVert)
            if len(sharedFace)==3:
                allFaces.remove(sharedFace)
        return allFaces
    cdef list removeTouchingTetra(self,Tetra.Tetrahedron tetrahe,list badTetra,list triangulation,(double,double,double,long int )point):
        cdef list myVert
        cdef list allfaces
        cdef list sharedWithOtherFaces
        cdef int firstIterator
        cdef int notSharedIterator
        cdef list allFacesHashes
        myVert=tetrahe.vertecies
        # print('vertecies',myVert)
        allfaces= [{myVert[0],myVert[1],myVert[2]},{myVert[0],myVert[1],myVert[3]},{myVert[3],myVert[1],myVert[2]},{myVert[0],myVert[3],myVert[2]}]
        sharedWithOtherFaces=[]
        for firstIterator in range(0,len(badTetra)):
            if len(allfaces)>0 and badTetra[firstIterator]!=tetrahe: 
                # print('tetra',badTetra[firstIterator].vertecies)
                allfaces=self.removeSharedFace(myVert,badTetra[firstIterator].vertecies,allfaces)          
        for notSharedIterator in range(0,len(allfaces)):
            first, second,third = allfaces[notSharedIterator]
            testTetra=Tetra.Tetrahedron(first,second,third,point)

            triangulation.append(testTetra)
        triangulation.remove(tetrahe)
        return triangulation
    cdef Tetra.Tetrahedron createSuperTetra(self,double length):
        cdef (double,double,double,long int) A
        cdef (double,double,double,long int) B
        cdef (double,double,double,long int) C
        cdef (double,double,double,long int) D
        A=(-3*length,0,-100*2*length,0)
        B=(3*length/sqrt(2),3*length/sqrt(2),-100*2*length,1)
        C=(3*length/sqrt(2),-3*length/sqrt(2),-100*2*length,2)
        D=(0,0,100*2*length,3)
        return Tetra.Tetrahedron(A,B,C,D)
    cdef bint liesOnSuper(self,list vert):
        return len(np.intersect1d(vert, self.superTetra.vertecies))>2
    cdef list computeTrianglePoints(self):
        cdef list triangulation
        cdef list filteredTriangulation
        cdef double totalStartTime
        cdef double firstTime
        cdef double secondTime
        cdef double firstT
        cdef double firstET
        cdef double totalEndTime
        cdef double totTime
        
        cdef long int idx 
        cdef list badTetra
        cdef Tetra.Tetrahedron tetrahe
        cdef long int tetraheIdx
        cdef long int iterator
        triangulation=[] #all triangles go here
        triangulation.append(self.superTetra)
        totalStartTime=time.time()
        firstTime=0
        secondTime=0
        for idx in range(0,len(self.pointSet)):
            if idx%100==0:
                print('Procent ukonczenia ',idx*100/len(self.pointSet),'%')
            firstT=time.time()
            badTetra=[]
            
            for iterator in range(0,len(triangulation)):
                if self.calcDistance(triangulation[iterator].O,self.pointSet[idx])<triangulation[iterator].R:
                    badTetra.append(triangulation[iterator])
            firstET=time.time()
            firstTime+=(firstET-firstT)
            firstT=time.time()
            badTetra=sorted(badTetra,key=lambda x: sum(x.vertecies[0])+sum(x.vertecies[1])+sum(x.vertecies[2])+sum(x.vertecies[3]))
            for tetrahe in badTetra: #here we check if our tetrahedra touches with other ones
                triangulation=self.removeTouchingTetra(tetrahe,badTetra,triangulation,self.pointSet[idx]) #prepared for multiprocess
            firstET=time.time()
            secondTime+=firstET-firstT
        totalEndTime=time.time()
        totTime=totalEndTime-totalStartTime
        print('totaj time',totTime,'first time percentage',firstTime*100/totTime,'%',"second time ",secondTime*100/totTime,'%')

                
            
        filteredTriangulation=[]
        for tetrahe in triangulation:
            if not self.liesOnSuper(tetrahe.vertecies):
                filteredTriangulation.append(tetrahe)

        
        return filteredTriangulation
    cdef  double calcDistance(self,( double, double, double) A,( double, double, double,long int) B):
        cdef double calculated
        cdef double suma
        suma=sqrt( pow(A[0]-B[0],2)+pow(A[1]-B[1],2)+pow(A[2]-B[2],2) ) 
        return suma
    cdef set compareTetraFaces(self,list vertA,list vertB):
        cdef set face
        face=set(vertB).intersection(set(vertA)) #how many verticies are the same
        return face

    cdef list transformToIndexes(self):
        #adding indexes instead of values
        cdef list verticiesIndex
        cdef Tetra.Tetrahedron tetra
        cdef list tetraTuple
        cdef list newRow
        cdef long int idx
        cdef long int indx
        cdef (double,double,double) xyz
        cdef (double,double,double) tup
        verticiesIndex=[]
        for tetra in self.tetraPoints:
            newRow=[ tetra.A[3],tetra.B[3],tetra.C[3],tetra.D[3]]
            verticiesIndex.append(newRow)
        return verticiesIndex

    cdef list computerVertexCoordsFacesColors(self):
        cdef list xyz
        cdef list faces
        cdef list colors
        cdef list vert
        cdef list vertexComb
        
        cdef long int index
        cdef (long int,long int,long int) p
        cdef (double,double,double,long int) myPt
        cdef (int,int,int) myFaceColor

        xyz=[]
        faces=[]
        colors=[]
        for vert in self.transformed:
            for index in vert:
                myPt=self.pointSet[index]
                xyz.append([myPt[0],myPt[1],myPt[2]])
            vertexComb=[(vert[0],vert[1],vert[2]),(vert[0],vert[1],vert[3]),(vert[3],vert[1],vert[2]),(vert[0],vert[3],vert[2])]
            for p in vertexComb: #adding faces of tetrahedra
                faces.append(p)
            myFaceColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            colors.append(myFaceColor)#same color for each face of tetra
            colors.append(myFaceColor)
            colors.append(myFaceColor)
            colors.append(myFaceColor)
        total=[xyz,faces,colors]
        return total
    cpdef computeVertices(self):
        self.tetraPoints=self.computeTrianglePoints()
        self.transformed=self.transformToIndexes()  #transform values of points ,to indexes of them in main point set
        return self.transformed,self.tetraPoints
    cdef list computeNormals(self,list faces,list points):
        cdef list normals
        cdef (long int,long int,long int) face
        cdef list p1
        cdef list p2
        cdef list p3
        cdef np.ndarray N
        normals=[]
        for face in faces:
            p1=points[face[0]]
            p2=points[face[1]]
            p3=points[face[2]]
            N = np.cross(np.subtract(p2,p1),np.subtract(p3,p1))
            normals.append(N)
        return normals
    cpdef plotSelf(self):
        cdef list fullPoints
        cdef list total
        cdef list normals

        fullPoints=[]
        total=self.computerVertexCoordsFacesColors()
        xyz=total[0]
        faces=total[1]
        colors=total[2]
        #normals=self.computeNormals(faces,xyz)  
        return [xyz,faces,colors]
        




