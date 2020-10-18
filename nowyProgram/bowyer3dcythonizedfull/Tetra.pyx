import numpy as numpy
cimport numpy
import scipy
from libc.math cimport sqrt,pow
import SphereCenterCython
cdef class Tetrahedron():
    # cdef public:
    #     cdef (double,double,double) A
    #     cdef (double,double,double) B
    #     cdef (double,double,double) C
    #     cdef (double,double,double) D
    #     cdef double R
    #     cdef (double,double,double) O
    #     cdef list vertecies
    def __cinit__(self,(double,double,double) Agiven,(double,double,double) Bgiven,(double,double,double) Cgiven,(double,double,double) Dgiven): 
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
        output=self.calcCenter(self.A,self.B,self.C,self.D)
        x0=output[0]
        y0=output[1]
        z0=output[2]
        return [(x0,y0,z0),self.dist((x0,y0,z0),self.A)]
    cdef list calcCenter(self,( double, double, double) A,( double, double, double) B,( double, double, double) C,( double, double, double) D):
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
            [A[0],A[1],A[2],1],
            [B[0],B[1],B[2],1],
            [C[0],C[1],C[2],1],
            [D[0],D[1],D[2],1]])
        a=scipy.linalg.det(first)
        firstSquare=A[0]**2+A[1]**2+A[2]**2
        secondSquare=B[0]**2+B[1]**2+B[2]**2
        thirdSquare=C[0]**2+C[1]**2+C[2]**2
        forthSquare=D[0]**2+D[1]**2+D[2]**2

        
        matindexes=[[1,2],[0,2],[0,1]]
        determinants=[]
        for indexes in range(0,len(matindexes)):
            determinants.append(self.calcDet(matindexes[indexes],firstSquare,secondSquare,thirdSquare,forthSquare,A,B,C,D))

        x0=determinants[0]/(2*a)
        y0=-determinants[1]/(2*a)
        z0=determinants[2]/(2*a)
        output=[x0,y0,z0]
        return output
    cdef  double calcDet(self,list indexes, double firstSquare, double  secondSquare, double  thirdSquare, double  forthSquare,( double, double, double) A,( double, double, double) B,( double, double, double) C, ( double, double, double) D):
        cdef numpy.ndarray mat
        mat= numpy.array([
                [firstSquare,A[indexes[0]],A[indexes[1]],1],
                [secondSquare,B[indexes[0]],B[indexes[1]],1],
                [thirdSquare,C[indexes[0]],C[indexes[1]],1],
                [forthSquare,D[indexes[0]],D[indexes[1]],1]])
        return scipy.linalg.det(mat)
    cdef bint pointInSphere(self,(double,double,double) point):
        cdef double distance 
        distance=self.dist(self.O,point)
        return distance<=self.R
    cdef double dist(self,( double, double, double) p1,( double, double, double) p2):
        cdef double val
        val=sqrt( pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2) )
        return val
    cdef bint HasVertex(self,(double,double,double) point):
        return point in self.vertecies     

