from distutils.core import Extension, setup
from Cython.Build import cythonize
import numpy

# define an extension that will be cythonized and compiled
sphcent = Extension(name="SphereCenterCython", sources=["SphereCenterCython.pyx"])
dis = Extension(name="DistanceCython", sources=["DistanceCython.pyx"])
mylist=[sphcent,dis]
setup(ext_modules=cythonize(mylist),include_dirs=[numpy.get_include()])
