import numpy
cimport numpy
import scipy
from libc.math cimport sqrt,pow

cdef  double calcDistance(( double, double, double) A,( double, double, double) B):
    cdef double calculated
    cdef double suma
    suma=sqrt( pow(A[0]-B[0],2)+pow(A[1]-B[1],2)+pow(A[2]-B[2],2) ) 
    return suma
cpdef dist(( double, double, double) p1,( double, double, double) p2):
    cdef double wynik
    wynik=calcDistance(p1,p2)
    return wynik