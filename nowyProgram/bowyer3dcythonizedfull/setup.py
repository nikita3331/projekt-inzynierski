from distutils.core import Extension, setup
from Cython.Build import cythonize
import numpy

# define an extension that will be cythonized and compiled
sphcent = Extension(name="SphereCenterCython", sources=["SphereCenterCython.pyx"])
dis = Extension(name="DistanceCython", sources=["DistanceCython.pyx"])
pt = Extension(name="PointInAllTetra", sources=["PointInAllTetra.pyx"])
smallTetraLoop=Extension(name="CreateNewTetra", sources=["CreateNewTetra.pyx"])
tetra=Extension(name="Tetra", sources=["Tetra.pyx"])
delaunay=Extension(name="MyDelaunay", sources=["MyDelaunay.pyx"])

mylist=[sphcent,dis,pt,smallTetraLoop,tetra,delaunay]
setup(ext_modules=cythonize(mylist),include_dirs=[numpy.get_include()])
