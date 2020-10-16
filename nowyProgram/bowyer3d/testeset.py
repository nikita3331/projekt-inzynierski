import numpy as np
from Point3D import Point
import collections
import itertools
import timeit
from operator import itemgetter
import time


def findWithMinus(A,B):
    sA=set(A)
    sB=set(B)
    face=sB.intersection(sA)
    return face

def simulate(A,badTetra):
    startFirst=time.time()
    allfaces=[{A[0],A[1],A[2]},{A[0],A[1],A[3]},{A[3],A[1],A[2]},{A[0],A[3],A[2]}]
    endFirst=time.time()
    
    startSecond=time.time()
    for other in badTetra:
        sharedFace=findWithMinus(A,other)
        if len(sharedFace)==3:
            allfaces.remove(sharedFace)  
    endSecond=time.time()
    

    newFac=[]
    startThird=time.time()
    for notSharedFace in allfaces:
        first, second,third = notSharedFace
        newFac.append((first,second,third,(200,200,200)))
    endThird=time.time()
    
    return newFac,endFirst-startFirst,endSecond-startSecond,endThird-startThird





def trackTime(a,tetra):
    meanFirst=0
    meanSecond=0
    meanThird=0
    ran=10
    firstTime=0
    secondTime=0
    thirdTime=0
    startTotalRun=time.time()
    for j in range(0,ran):
        startFull=time.time()
        fFull=0
        sFull=0
        tFull=0
        for i in range(0,10000):
            _,f,s,t=simulate(a,tetra)
            fFull+=f
            sFull+=s
            tFull+=t
        end=time.time()
        total=end-startFull
        firstTime+=fFull
        secondTime+=sFull
        thirdTime+=tFull
        firstPercent=fFull*100/total
        secondPercent=sFull*100/total
        thirdPercent=tFull*100/total
        meanFirst+=firstPercent
        meanSecond+=secondPercent
        meanThird+=thirdPercent
    endTotalRun=time.time()

    timFirst=firstTime/(ran*100000)
    timSecond=secondTime/(ran*100000)
    timThird=thirdTime/(ran*100000)
    totFirst=meanFirst/ran
    totSecond=meanSecond/ran
    totThird=meanThird/ran
    totalTime=endTotalRun-startTotalRun
    print('wykonane operacje calkowity czas',totalTime,timFirst*1000,'ms',totFirst,'% ',timSecond*1000,'ms',totSecond,' %',timThird*1000,'ms',totThird,' %')




if __name__ == '__main__':
    a=[(10,15,17),(1,2,3),(7,8,9),(4,5,6)]
    b=[(4,5,6),(1,2,3),(7,8,9),(9,11,12)]
    vala=[ ( (4,5,6),(1,2,3), (1,2,3) ),( (4,5,6), (4,5,6), (4,5,6) ) ] 
    valb=(  (1,2,3),(4,5,6),(1,2,3) )

    newa=[{(1,2,3),(4,5,6),(1,2,4)},{3,4}]



    tetra=[[(7,3,7),(1,2,3),(7,8,9),(4,5,6)],[(10,15,17),(1,2,3),(22,29,38),(4,5,6)],[(10,15,17),(1,2,3),(28,29,31),(100,99,98)]]
    first=[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
    second=[[1,2,3],[7,8,9],[10,11,12],[53,54,33]]


    trackTime(a,tetra)
    #faces,_,_,_=simulate(a,tetra)
    # print(faces)

    # count(100)




