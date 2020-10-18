cdef class Tetrahedron:
    cdef public:
        cdef (double,double,double) A
        cdef (double,double,double) B
        cdef (double,double,double) C
        cdef (double,double,double) D
        cdef double R
        cdef (double,double,double) O
        cdef list vertecies
        cdef list calculateSphereCenter(Tetrahedron)
        cdef list calcCenter(Tetrahedron,( double, double, double),( double, double, double),( double, double, double),( double, double, double))
        cdef  double calcDet(Tetrahedron,list, double, double, double, double ,( double, double, double) ,( double, double, double) ,( double, double, double) , ( double, double, double) )
        cdef bint pointInSphere(Tetrahedron,(double,double,double))
        cdef double dist(Tetrahedron,( double, double, double),( double, double, double))
        cdef bint HasVertex(Tetrahedron,(double,double,double))