import numpy as numpy
cimport numpy
import scipy
from libc.math cimport sqrt,pow
cdef class Tetrahedron(): #klasa zawierająca funkcje pomocnicze przy generacji ostrosłupów. Przechowuje informacje na temat wierzchołków i ścian ostrosłupa. 

    def __cinit__(self,(double,double,double,long int) Agiven,(double,double,double,long int) Bgiven,(double,double,double,long int) Cgiven,(double,double,double,long int) Dgiven): 
        self.A=Agiven
        self.B=Bgiven
        self.C=Cgiven
        self.D=Dgiven
        self.vertecies=[self.A,self.B,self.C,self.D]
        cdef list out
        out=self.calculateSphereCenter() #wyznaczanie środka sfery opisanej na strosłupie oraz jej promienia
        self.O=out[0] #środek sfery
        self.R=out[1] #jej promień
        
    cdef list calculateSphereCenter(self): #wyznaczanie współrzędnych środka sfery opisanej na strosłupie wraz z jej promieniem
        output=self.calcCenter()
        x0=output[0]
        y0=output[1]
        z0=output[2]
        return [(x0,y0,z0),self.dist((x0,y0,z0),self.A)]
    cdef list calcCenter(self): #wyznaczanie środka sfery odbywa się na podstawie wzorów w poniższych odnośnikach. Zostały one omówione dokładniej w pracy.
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
        a=scipy.linalg.det(first) #scipy okazął się być lepszy do obliczenia wyznacznika niż numpy
        if abs(a)==0:
            return [self.A[0],self.A[1],self.A[2]]
        else:
            # w celu optymalizacji wartości te są wyznaczane tylko raz, następnie podawane jako parametr do liczenia wyznacznika
            firstSquare=self.A[0]**2+self.A[1]**2+self.A[2]**2
            secondSquare=self.B[0]**2+self.B[1]**2+self.B[2]**2
            thirdSquare=self.C[0]**2+self.C[1]**2+self.C[2]**2
            forthSquare=self.D[0]**2+self.D[1]**2+self.D[2]**2

            
            matindexes=[[1,2],[0,2],[0,1]] #jakie współrzędne punktów brane są pod uwagę przy liczeniu wyznaczników Dx,Dy,Dz ,odpowiednio YZ,XZ,XY
            determinants=[]
            for indexes in range(0,len(matindexes)):
                determinants.append(self.calcDet(matindexes[indexes],firstSquare,secondSquare,thirdSquare,forthSquare)) #wyznaczniki wpisane do macierzy

            #podstawiając do wzoru
            x0=determinants[0]/(2*a) 
            y0=-determinants[1]/(2*a)
            z0=determinants[2]/(2*a)
            output=[x0,y0,z0]
            return output

    cdef  double calcDet(self,list indexes, double firstSquare, double  secondSquare, double  thirdSquare, double  forthSquare): #pojedynczy wyznacznik Dx,Dy,Dz
        cdef numpy.ndarray mat
        mat= numpy.array([
                [firstSquare,self.A[indexes[0]],self.A[indexes[1]],1],
                [secondSquare,self.B[indexes[0]],self.B[indexes[1]],1],
                [thirdSquare,self.C[indexes[0]],self.C[indexes[1]],1],
                [forthSquare,self.D[indexes[0]],self.D[indexes[1]],1]])
        return scipy.linalg.det(mat) 
    cdef bint pointInSphere(self,(double,double,double,long int) point): #funkcja pomocnicza do głównej klasy, sprawdzanie przynależności puntu do sfery
        cdef double distance 
        distance=self.dist(self.O,point)
        return distance<=self.R
    cdef double dist(self,( double, double, double) p1,( double, double, double,long int) p2):#wyznaczanie odległości
        cdef double val
        val=sqrt( pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2) )
        return val


