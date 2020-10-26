import numpy as np
from scipy import linalg
import math
from Point3D import Point
import itertools
from multiprocessing import Process, Manager,Pool
from DistanceCython import dist
import SphereCenterCython
import time
class Tetrahedron():
    def __init__(self,A,B,C,D): #big A is point,small a is vertice
        self.A=A
        self.B=B
        self.C=C
        self.D=D
        self.vertecies=[self.A,self.B,self.C,self.D]
        self.O,self.R=self.calculateSphereCenter()
    def calcDet( self,indexes,  firstSquare,   secondSquare,   thirdSquare,   forthSquare):
        mat= np.array([
                [firstSquare,self.A[indexes[0]],self.A[indexes[1]],1],
                [secondSquare,self.B[indexes[0]],self.B[indexes[1]],1],
                [thirdSquare,self.C[indexes[0]],self.C[indexes[1]],1],
                [forthSquare,self.D[indexes[0]],self.D[indexes[1]],1]])
        return linalg.det(mat)
    def calcCenter(self):
        #https://arxiv.org/pdf/1805.08831.pdf
        #https://mathworld.wolfram.com/Circumsphere.html

        first= np.array([
            [self.A[0],self.A[1],self.A[2],1],
            [self.B[0],self.B[1],self.B[2],1],
            [self.C[0],self.C[1],self.C[2],1],
            [self.D[0],self.D[1],self.D[2],1]])
        a=linalg.det(first)
        firstSquare=self.A[0]**2+self.A[1]**2+self.A[2]**2
        secondSquare=self.B[0]**2+self.B[1]**2+self.B[2]**2
        thirdSquare=self.C[0]**2+self.C[1]**2+self.C[2]**2
        forthSquare=self.D[0]**2+self.D[1]**2+self.D[2]**2

        
        matindexes=[[1,2],[0,2],[0,1]]
        determinants=[]
        for indexes in matindexes:
            determinants.append(self.calcDet(indexes,firstSquare,secondSquare,thirdSquare,forthSquare))
        denominator=1/(2*a)
        x0=determinants[0]*denominator
        y0=-determinants[1]*denominator
        z0=determinants[2]*denominator
        output=[x0,y0,z0]
        return output
    def dist(self,p1,p2):
        suma=math.sqrt( math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2)+math.pow(p1[2]-p2[2],2) ) 
        return suma
    def calculateSphereCenter(self):
        output=self.calcCenter()
        x0=output[0]
        y0=output[1]
        z0=output[2]
        return (x0,y0,z0),self.dist((x0,y0,z0),self.A)
    def pointInSphere(self,point):
        distance=self.dist(self.O,point)
        return distance<=self.R
    def printSelf(self):
        print(self.vertecies)
        
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

