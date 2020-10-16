import numpy as np
import math
from Point3D import Point
import itertools

class Tetrahedron():
    def __init__(self,A,B,C,D): #big A is point,small a is vertice
        self.A=A
        self.B=B
        self.C=C
        self.D=D
        self.vertecies=[self.A,self.B,self.C,self.D]
        self.O,self.R=self.calculateSphereCenter()
    def dist(self,p1,p2):
        distance=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2) 
        return distance

    def calculateSphereCenter(self):
        #https://arxiv.org/pdf/1805.08831.pdf
        #https://mathworld.wolfram.com/Circumsphere.html
        first= np.matrix([
            [self.A[0],self.A[1],self.A[2],1],
            [self.B[0],self.B[1],self.B[2],1],
            [self.C[0],self.C[1],self.C[2],1],
            [self.D[0],self.D[1],self.D[2],1]])
        a=np.linalg.det(first)
        firstSquare=self.A[0]**2+self.A[1]**2+self.A[2]**2
        secondSquare=self.B[0]**2+self.B[1]**2+self.B[2]**2
        thirdSquare=self.C[0]**2+self.C[1]**2+self.C[2]**2
        forthSquare=self.D[0]**2+self.D[1]**2+self.D[2]**2
        
        matdx= np.matrix([
            [firstSquare,self.A[1],self.A[2],1],
            [secondSquare,self.B[1],self.B[2],1],
            [thirdSquare,self.C[1],self.C[2],1],
            [forthSquare,self.D[1],self.D[2],1]])
        dx=np.linalg.det(matdx)
        matdy= np.matrix([
            [firstSquare,self.A[0],self.A[2],1],
            [secondSquare,self.B[0],self.B[2],1],
            [thirdSquare,self.C[0],self.C[2],1],
            [forthSquare,self.D[0],self.D[2],1]])
        dy=-np.linalg.det(matdy)
        matdz= np.matrix([
            [firstSquare,self.A[0],self.A[1],1],
            [secondSquare,self.B[0],self.B[1],1],
            [thirdSquare,self.C[0],self.C[1],1],
            [forthSquare,self.D[0],self.D[1],1]])
        dz=np.linalg.det(matdz)
        x0=dx/(2*a)
        y0=dy/(2*a)
        z0=dz/(2*a)
        return (x0,y0,z0),self.dist((x0,y0,z0),self.A)
    def pointInSphere(self,point):
        distance=self.dist(self.O,point)
        return distance<=self.R

        


        
        
    @classmethod
    def createSuperTetra(cls,length):
        A=(-3*length,0,-100*2*length)
        B=(3*length/math.sqrt(2),3*length/math.sqrt(2),-100*2*length)
        C=(3*length/math.sqrt(2),-3*length/math.sqrt(2),-100*2*length)
        D=(0,0,100*2*length)
        superTri=cls(A,B,C,D) 
        return superTri

    def HasVertex(self,point):
        return point in self.vertecies     

