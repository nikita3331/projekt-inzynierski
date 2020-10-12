import numpy as np
from Point3D import Point
import collections
import itertools
import timeit
from operator import itemgetter


def findCurrVer(aVert,badTetra):
    faces= list(itertools.combinations(aVert, 3))
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    newFaces=[]
    for face in faces:
        isShared = False
        for otherVert in badTetra:
            otherFaces= list(itertools.combinations(otherVert, 3))
            if not isShared:
                for otherFace in otherFaces:
                    if compare(face,otherFace):
                        isShared = True
        if not isShared:
            newFaces.append((face[0],face[1],face[2],(200,200,200)))
    return newFaces
def findWithMinus(A,B):
    dele=set (B ) - set(A)
    face=[]
    if dele!=set(B) and len(dele)==1:
        face=tuple(set(B)-dele)
    return face
def simulate(A,badTetra,chosenType):
    allfaces=list(itertools.combinations(A, 3))
    buff=[]
    if chosenType==1:
        for face in allfaces:
            buff.append(set(face))
        allfaces=buff
        sharedWithOtherFaces=[]


        for other in badTetra:
            sharedFace=findWithMinus(A,other)
            if sharedFace!=[]:
                sharedWithOtherFaces.append(set(sharedFace))
        #-----------------------------------        
        # notshared=[]
        # for allFace in allfaces: 
        #     toremove=False
        #     for sharedFaceItem in sharedWithOtherFaces:
        #         if (sharedFaceItem[0] in allFace) and (sharedFaceItem[1] in allFace) and (sharedFaceItem[2] in allFace):
        #             toremove=True
        #     if not toremove:
        #         notshared.append(allFace)
        # newfaces=[]# creating new tetra
        # for item in notshared:
        #     newfaces.append((item[0],item[1],item[2],(200,200,200)))
        #-----------------------------------        
        for sharedFaceItem in sharedWithOtherFaces:#performing allfaces-sharedfaces
            allfaces.remove(sharedFaceItem)
        newFac=[]
        for notSharedFace in allfaces:
            listed=list(notSharedFace)
            newFac.append((listed[0],listed[1],listed[2],(200,200,200)))
    else:
        sharedWithOtherFaces=[]
        for other in badTetra:
            sharedFace=findWithMinus(A,other)
            if sharedFace!=[]:
                sharedWithOtherFaces.append(sharedFace)
        #-----------------------------------        
        notshared=[]
        for allFace in allfaces: 
            toremove=False
            for sharedFaceItem in sharedWithOtherFaces:
                if (sharedFaceItem[0] in allFace) and (sharedFaceItem[1] in allFace) and (sharedFaceItem[2] in allFace):
                    toremove=True
            if not toremove:
                notshared.append(allFace)
        newFac=[]# creating new tetra
        for item in notshared:
            newFac.append((item[0],item[1],item[2],(200,200,200)))
    
    return newFac





if __name__ == '__main__':
    a=[(10,15,17),(1,2,3),(7,8,9),(4,5,6)]
    b=[(4,5,6),(1,2,3),(7,8,9),(9,11,12)]
    vala=[ ( (4,5,6),(1,2,3), (1,2,3) ),( (4,5,6), (4,5,6), (4,5,6) ) ] 
    valb=(  (1,2,3),(4,5,6),(1,2,3) )

    newa=[{(1,2,3),(4,5,6),(1,2,4)},{3,4}]



    tetra=[[(7,3,7),(1,2,3),(7,8,9),(4,5,6)],[(10,15,17),(1,2,3),(22,29,38),(4,5,6)],[(10,15,17),(1,2,3),(28,29,31),(100,99,98)]]

    print('sredni czas starego',timeit.timeit("simulate(a,tetra,1)", setup="from __main__ import simulate,a,tetra",number=1000)*1000/2,'ms')
    print('sredni czas nowego',timeit.timeit("simulate(a,tetra,0)", setup="from __main__ import simulate,a,tetra",number=1000)*1000/2,'ms')


    # count(100)




