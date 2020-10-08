from random import random
arr=[]
for i in range(0,30):
    point=(random()*100,random()*100,random()*100)
    arr.append(point)
for item in arr:
    print('Point'+str(item),end=',')