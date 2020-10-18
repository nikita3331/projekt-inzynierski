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
    def calculateSphereCenter(self):
        output=SphereCenterCython.calcCenter(self.A,self.B,self.C,self.D)
        x0=output[0]
        y0=output[1]
        z0=output[2]
        return (x0,y0,z0),dist((x0,y0,z0),self.A)
    def pointInSphere(self,point):
        distance=dist(self.O,point)
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

