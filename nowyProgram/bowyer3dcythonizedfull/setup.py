from distutils.core import Extension, setup
from Cython.Build import cythonize
import numpy

# define an extension that will be cythonized and compiled

tetra=Extension(name="Tetra", sources=["Tetra.pyx"])
delaunay=Extension(name="MyDelaunay", sources=["MyDelaunay.pyx"])

mylist=[tetra,delaunay]
setup(ext_modules=cythonize(mylist),include_dirs=[numpy.get_include()])
