import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



x=np.linspace(100,200,100,dtype='int')
x[5]=0
x[10]=0
x[15]=0
x[20]=0
x[40]=0

indexesAll=[]
indexesWithoutEmpty=[]
valuesWithoutEmpty=[]
for idx,item in enumerate(x):
    if item!=0:
        indexesWithoutEmpty.append(idx)
        valuesWithoutEmpty.append(item)
    indexesAll.append(idx)
f = interp1d(indexesWithoutEmpty, valuesWithoutEmpty,kind='cubic')


filledValues=f(indexesAll)


beginPoints=[]
endPoints=[]

for it_x,idx,it_fill in zip(x,indexesAll,filledValues):
    beginPoints.append((idx,it_x))
    endPoints.append((idx,it_fill))

print(beginPoints)
print(endPoints)

plt.scatter(indexesAll,x,label='old set')
plt.plot(indexesAll,filledValues,label='new set')
plt.legend()
plt.show()