import numpy as np
import math
from Point import Point
class Triangle():
    def __init__(self,A,B,C): #big A is point,small a is vertice
        self.A=A
        self.B=B
        self.C=C
        self.edges=[(self.A,self.B),(self.B,self.A),(self.A,self.C),(self.C,self.A),(self.B,self.C),(self.C,self.B)]
        self.a=self.dist(self.B,self.C)
        self.b=self.dist(self.A,self.C)
        self.c=self.dist(self.B,self.A)
        self.p=(self.a+self.b+self.c)/2
        self.isTriangleBool=self.isTriangle()
        self.initValues()
        
    def printSelf(self):
        print('A = (',self.A.x,',',self.A.y,') B = (',self.B.x,',',self.B.y,') C = (',self.C.x,',',self.C.y,')')  
    def isTriangle(self):  
        if (self.B ==self.A) or (self.A == self.C) or (self.B == self.C) : 
            return False
        else: 
            return True
    def initValues(self):
        if self.isTriangleBool:
            self.r=self.innerCircle()
            self.R=self.circumCircleRadius()
            self.Rx0y0=self.findCenterOfBigCircle()
    def innerCircle(self): #wpisany w trojkat
        r=math.sqrt(  (self.p-self.a)*(self.p-self.b)*(self.p-self.c)/self.p )
        return r
    def circumCircleRadius(self):   #opisany na trojkacie
        R=(self.a*self.b*self.c)/(4*self.r*self.p)
        return R
    def findCenterOfBigCircle(self):
        #https://pl.wikipedia.org/wiki/Symetralna_odcinka
        ax=self.A.x
        ay=self.A.y
        
        bx=self.B.x
        by=self.B.y
        axminbx=ax-bx
        ayminby=ay-by
        rightAb=ax*axminbx+bx*axminbx+ay*ayminby+by*ayminby


        cx=self.C.x
        cy=self.C.y
        axmincx=ax-cx
        aymincy=ay-cy
        rightAc=ax*axmincx+cx*axmincx+ay*aymincy+cy*aymincy


        A = np.array( [[2*axminbx, 2*ayminby], [2*axmincx, 2*aymincy]])
        B = np.array([rightAb, rightAc])
        X = np.linalg.inv(A).dot(B)
        return Point(X[0],X[1])
    def pointInBigCircle(self,point):
        distance=self.dist(self.Rx0y0,point)
        return distance<=self.R
    def splitIntoTriangles(self,point):
        newtriangles=[]
        newtri=Triangle(self.A,self.B,point)
        if newtri.isTriangleBool:
            newtriangles.append(newtri)
        newtri=Triangle(self.A,point,self.C)
        if newtri.isTriangleBool:
            newtriangles.append(newtri)
        newtri=Triangle(point,self.B,self.C)
        if newtri.isTriangleBool:
            newtriangles.append(newtri)
        return newtriangles
    def dist(self,p1,p2):
        distance=math.sqrt( (p1.x-p2.x)**2+(p1.y-p2.y)**2 )
        return distance
    @classmethod
    def createSuperTriangle(cls,length):
        A=Point(-10*length,-length)
        B=Point(0,10*length)
        C=Point(10*length,-length)
        superTri=cls(A,B,C) 
        return superTri