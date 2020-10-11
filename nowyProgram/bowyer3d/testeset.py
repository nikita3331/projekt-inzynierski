import numpy as np
from Point3D import Point
import collections
import itertools
import timeit
from operator import itemgetter


def findNormal(A,B):
    aComb= list(itertools.combinations(A, 3))
    bComb= list(itertools.combinations(B, 3))
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    found=False
    faces=[]
    for idx,item in enumerate(aComb):
        if not found:
            for itemb in bComb:
                if compare(item,itemb):
                    faces=item
                    found=True
        else:
            continue
    return faces
def findWithMinus(A,B):
    crossed=np.abs(np.cross(A,B))
    #mydet=np.abs(np.linalg.det(Crossed))
    dele=set (B ) - set(A)
    faces=[]
    if dele!=set(B):
        faces=list(set(B)-dele)
    return faces



if __name__ == '__main__':
    a=[(10,15,17),(1,2,3),(7,8,9),(4,5,6)]
    b=[(4,5,6),(1,2,3),(7,8,9),(9,11,12)]
    print('sredni czas ',timeit.timeit("findNormal([(10,15,17),(1,2,3),(7,8,9),(4,5,6),(6,5,4),(3,3,2)],[(4,5,6),(1,2,3),(7,8,9),(9,11,12),(9,8,2),(11,20,21)])", setup="from __main__ import findNormal",number=10000)*1000/10,'ms')
    print('sredni czas ',timeit.timeit("findWithMinus([(10,15,17),(1,2,3),(7,8,9),(4,5,6),(6,5,4),(3,3,2)],[(4,5,6),(1,2,3),(7,8,9),(9,11,12),(9,8,2),(11,20,21)])", setup="from __main__ import findWithMinus",number=10000)*1000/10,'ms')
    # count(100)




