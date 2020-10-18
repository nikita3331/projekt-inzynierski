import numpy
cimport numpy
import scipy
from libc.math cimport sqrt,pow
from libc.math cimport sqrt,pow
from Tetra import Tetrahedron


cdef  list myloop(list allfaces,list triangulation,(double,double,double) point):
    cdef long int iterator
    cdef (double,double,double) first
    cdef (double,double,double) second
    cdef (double,double,double) third

    for iterator in range(0,len(allfaces)):
        first,second,third=allfaces[iterator]
        triangulation.append(Tetrahedron(first,second,third,point))
    return triangulation
cpdef tetraLoop(list allfaces,list triangulation,(double,double,double) point):
    cdef list wynik
    wynik=myloop(allfaces,triangulation,point)
    return wynik