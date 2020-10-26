cimport numpy

cdef class Tetrahedron:
    cdef public:
        cdef (double,double,double,long int) A #vert
        cdef (double,double,double,long int) B#vert
        cdef (double,double,double,long int) C#vert
        cdef (double,double,double,long int) D#vert
        cdef double R #circumsphere radius
        cdef (double,double,double) O #circumsphere center
        cdef list vertecies
        cdef list calculateSphereCenter(Tetrahedron)
        cdef list calcCenter(Tetrahedron)
        cdef list calcCenterOld(Tetrahedron)
        cdef  double calcDet(Tetrahedron,list, double, double, double, double)
        cdef bint pointInSphere(Tetrahedron,(double,double,double,long int))
        cdef double dist(Tetrahedron,( double, double, double),( double, double, double,long int))
        cdef bint HasVertex(Tetrahedron,(double,double,double,long int))