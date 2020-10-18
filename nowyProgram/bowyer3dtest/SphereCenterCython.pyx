import numpy
cimport numpy
import scipy

cdef  double calcDet(list indexes, double firstSquare, double  secondSquare, double  thirdSquare, double  forthSquare,( double, double, double) A,( double, double, double) B,( double, double, double) C, ( double, double, double) D):
    cdef numpy.ndarray mat
    mat= numpy.array([
            [firstSquare,A[indexes[0]],A[indexes[1]],1],
            [secondSquare,B[indexes[0]],B[indexes[1]],1],
            [thirdSquare,C[indexes[0]],C[indexes[1]],1],
            [forthSquare,D[indexes[0]],D[indexes[1]],1]])
    return scipy.linalg.det(mat)
cpdef calcCenter(( double, double, double) A,( double, double, double) B,( double, double, double) C,( double, double, double) D):
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
        determinants.append(calcDet(matindexes[indexes],firstSquare,secondSquare,thirdSquare,forthSquare,A,B,C,D))

    x0=determinants[0]/(2*a)
    y0=-determinants[1]/(2*a)
    z0=determinants[2]/(2*a)
    output=[x0,y0,z0]
    return output