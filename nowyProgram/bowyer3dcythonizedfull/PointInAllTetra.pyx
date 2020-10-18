import numpy
cimport numpy
import scipy
from libc.math cimport sqrt,pow
from libc.math cimport sqrt,pow

cdef  double calcDistance(( double, double, double) A,( double, double, double) B):
    cdef double calculated
    cdef double suma
    suma=sqrt( pow(A[0]-B[0],2)+pow(A[1]-B[1],2)+pow(A[2]-B[2],2) ) 
    return suma
cdef  list loopPointInTetra(( double, double, double) point,list triangulation):
    cdef long int iterator
    cdef list badtetra
    badtetra=[]
    for iterator in range(0,len(triangulation)):
        if calcDistance(triangulation[iterator].O,point)<triangulation[iterator].R:
            badtetra.append(triangulation[iterator])
    return badtetra
cpdef checkPoint(( double, double, double) point,list triangulation):
    cdef list wynik
    wynik=loopPointInTetra(point,triangulation)
    return wynik