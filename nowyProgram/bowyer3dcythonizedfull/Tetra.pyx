import numpy as numpy
cimport numpy
import scipy
print(scipy.__file__)
from libc.math cimport sqrt,pow,abs
cdef class Tetrahedron():

    def __cinit__(self,(double,double,double,long int) Agiven,(double,double,double,long int) Bgiven,(double,double,double,long int) Cgiven,(double,double,double,long int) Dgiven): 
        self.A=Agiven
        self.B=Bgiven
        self.C=Cgiven
        self.D=Dgiven
        self.vertecies=[self.A,self.B,self.C,self.D]
        cdef list out
        out=self.calculateSphereCenter()
        self.O=out[0]
        self.R=out[1]
        
    cdef list calculateSphereCenter(self):
        output=self.calcCenter()
        x0=output[0]
        y0=output[1]
        z0=output[2]
        return [(x0,y0,z0),self.dist((x0,y0,z0),self.A)]
    cdef list calcCenter(self):
        #https://arxiv.org/pdf/1805.08831.pdf
        #https://mathworld.wolfram.com/Circumsphere.html
        cdef numpy.ndarray first
        cdef  double a
        cdef  double firstSquare
        cdef  double secondSquare
        cdef  double thirdSquare
        cdef  double forthSquare
        cdef list matindexes
        cdef list determinants
        cdef  int indexes
        cdef double x0,y0,z0
        first= numpy.array([
            [self.A[0],self.A[1],self.A[2],1],
            [self.B[0],self.B[1],self.B[2],1],
            [self.C[0],self.C[1],self.C[2],1],
            [self.D[0],self.D[1],self.D[2],1]])
        a=scipy.linalg.det(first)

        firstSquare=self.A[0]**2+self.A[1]**2+self.A[2]**2
        secondSquare=self.B[0]**2+self.B[1]**2+self.B[2]**2
        thirdSquare=self.C[0]**2+self.C[1]**2+self.C[2]**2
        forthSquare=self.D[0]**2+self.D[1]**2+self.D[2]**2

        
        matindexes=[[1,2],[0,2],[0,1]]
        determinants=[]
        for indexes in range(0,len(matindexes)):
            determinants.append(self.calcDet(matindexes[indexes],firstSquare,secondSquare,thirdSquare,forthSquare))

        x0=determinants[0]/(2*a)
        y0=-determinants[1]/(2*a)
        z0=determinants[2]/(2*a)
        output=[x0,y0,z0]
        return output
    cdef list calcCenterOld(self):
        cdef numpy.ndarray u1 
        cdef numpy.ndarray u2
        cdef numpy.ndarray u3
        cdef numpy.ndarray first
        cdef numpy.ndarray second
        cdef numpy.ndarray third
        cdef numpy.ndarray top
        cdef double bottom 
        cdef numpy.ndarray divided
        cdef numpy.ndarray sumed

        
        
        cdef  double e
        cdef  double f
        cdef  double g

        e=self.dist((self.D[0],self.D[1],self.D[2]),self.A)
        f=self.dist((self.D[0],self.D[1],self.D[2]),self.B)
        g=self.dist((self.D[0],self.D[1],self.D[2]),self.C)

        u2=numpy.array(self.A)-numpy.array(self.D)
        u3=numpy.array(self.C)-numpy.array(self.D)
        u1=numpy.array(self.B)-numpy.array(self.D)
        first= (f**2)*numpy.cross(u2[0:3],u3[0:3])
        second= (e**2)*numpy.cross(u3[0:3],u1[0:3])
        third= (g**2)*numpy.cross(u1[0:3],u2[0:3])

        top=first+second+third
        bottom=  numpy.dot(2*u1[0:3],numpy.cross(u2[0:3],u3[0:3]))
        divided=top/bottom
        sumed=numpy.array([self.D[0],self.D[1],self.D[2]])+divided

        output=[sumed[0],sumed[1],sumed[2]]
        return output
    cdef  double calcDet(self,list indexes, double firstSquare, double  secondSquare, double  thirdSquare, double  forthSquare):
        cdef numpy.ndarray mat
        mat= numpy.array([
                [firstSquare,self.A[indexes[0]],self.A[indexes[1]],1],
                [secondSquare,self.B[indexes[0]],self.B[indexes[1]],1],
                [thirdSquare,self.C[indexes[0]],self.C[indexes[1]],1],
                [forthSquare,self.D[indexes[0]],self.D[indexes[1]],1]])
        return scipy.linalg.det(mat) 
    cdef bint pointInSphere(self,(double,double,double,long int) point):
        cdef double distance 
        distance=self.dist(self.O,point)
        return distance<=self.R
    cdef double dist(self,( double, double, double) p1,( double, double, double,long int) p2):
        cdef double val
        val=sqrt( pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2) )
        return val
    cdef bint HasVertex(self,(double,double,double,long int) point):
        return point in self.vertecies     

