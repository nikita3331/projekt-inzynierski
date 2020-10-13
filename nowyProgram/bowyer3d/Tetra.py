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
        self.a=self.dist(self.B,self.C)
        self.b=self.dist(self.A,self.C)
        self.c=self.dist(self.B,self.A)
        self.e=self.dist(self.D,self.A)
        self.f=self.dist(self.D,self.B)
        self.g=self.dist(self.D,self.C)
        self.p=(self.a+self.b+self.c)/2
        self.isValidTetra=self.checkValid()
        self.initValues()
    def printSelf(self):
        print('A = ',self.A.toArr(),'B = ',self.B.toArr(),'C = ',self.C.toArr(),'D = ',self.D.toArr())
    def dist(self,p1,p2):
        distance=math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2+(p1.z-p2.z)**2) 
        return distance
    def checkValid(self):
        u=self.D.toArr()-self.A.toArr()
        v=self.D.toArr()-self.C.toArr()
        w=self.D.toArr()-self.B.toArr()
        insides=np.dot(u,np.cross(v,w)) 
        if insides!=0:
            return True
        else:
            return False
    def circumCircleCenter(self):
        u2=self.A.toArr()-self.D.toArr()
        u3=self.C.toArr()-self.D.toArr()
        u1=self.B.toArr()-self.D.toArr()
        first= (self.f**2)*np.cross(u2,u3)
        second= (self.e**2)*np.cross(u3,u1)
        third= (self.g**2)*np.cross(u1,u2)

        top=first+second+third
        bottom=  np.dot(2*u1,np.cross(u2,u3)) 
        divided=top/bottom
        sumed=self.D.toArr()+divided
        return Point(sumed[0],sumed[1],sumed[2])
    def pointInSphere(self,point):
        if self.isValidTetra:
            distance=self.dist(self.O,point)
            return distance<=self.R
        else:
            return False
        
    def initValues(self):
        if self.isValidTetra:
            self.O=self.circumCircleCenter()
            self.R=self.dist(self.O,self.A)
    @classmethod
    def createSuperTetra(cls,length):
        A=Point(-3*length,0,-100*2*length)
        B=Point(3*length/math.sqrt(2),3*length/math.sqrt(2),-100*2*length)
        C=Point(3*length/math.sqrt(2),-3*length/math.sqrt(2),-100*2*length)
        D=Point(0,0,100*2*length)
        superTri=cls(A,B,C,D) 
        return superTri

    def HasVertex(self,point):
        return (self.A == point) or (self.B == point) or (self.C == point) or (self.D == point)     

