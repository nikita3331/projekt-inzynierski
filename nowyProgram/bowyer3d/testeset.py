import numpy as np
from Point3D import Point
import collections
import itertools

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
a=[(1,2,3),2,1,4]
b=[1,4,(1,2,3),5]
aComb= list(itertools.combinations(a, 3))
bComb= list(itertools.combinations(b, 3))

found=False
for idx,item in enumerate(aComb):
    if not found:
        for itemb in bComb:
            if compare(item,itemb):
                print('found on ',idx,' items ',item,itemb)
                found=True
    else:
        continue
    print(idx)
print(aComb,bComb)
print(compare(a,b))

