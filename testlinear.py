import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



def cubic(arr):
    indexesAll=[]
    indexesWithoutEmpty=[]
    valuesWithoutEmpty=[]
    for idx,item in enumerate(arr):
        if item!=0:
            indexesWithoutEmpty.append(idx)
            valuesWithoutEmpty.append(item)
        indexesAll.append(idx)
    f = interp1d(indexesWithoutEmpty, valuesWithoutEmpty,kind='cubic')
    return f(indexesAll)
myarr=[10**4,20**4,0,40**4,50**4,60**4,0,90**4]
true=[(i*10)**4 for i in range(1,9)]
filed=cubic(myarr)
error=(filed-true)*100/filed
print(error)



