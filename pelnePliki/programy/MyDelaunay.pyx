cimport numpy as np
import numpy as np
from libc.math cimport sqrt,pow
from Point3D import Point
cimport Tetra
import random
import time

cdef class Delaunay():
    #https://math.stackexchange.com/questions/2414640/circumsphere-of-a-tetrahedron
    cdef public: #Deklaracja zmiennych używanych wewnątrz klasy
        cdef list pointSet
        cdef list vertices
        cdef list trianglePoints
        cdef list tetraPoints
        cdef list transformed
        cdef object updateProcess
        cdef Tetra.Tetrahedron superTetra
    def __init__(self,list pointSet,object updateProcess): 
        self.pointSet=pointSet #zbiór punktów do triangulacji
        self.vertices=[]    #wierzchołki trójkątów, zapisane w postaci indeksów
        self.trianglePoints=[]  #wierzchołki wygenerowanych ostrosłupów
        self.updateProcess=updateProcess
        self.superTetra=self.createSuperTetra(10000) #utworzenie super-ostrosłupa, zawierającego wszystkie punkty poddawane obróbce
    cdef list removeSharedFace(self,list myVert,list otherVert,list allFaces): #usuwanie ścian współdzielonych z pozostałymi ostrosłupami
        cdef set sharedFace
        if len(allFaces)>0:
            sharedFace=self.compareTetraFaces(myVert,otherVert) #sprawdzanie czy kombinacja wierzchołków tworzy wspólną ścianę
            if len(sharedFace)==3:  #dla 3 wierzchołków można utworzyć ścianę
                allFaces.remove(sharedFace) #jest ona usuwana z dostępnych ścian
        return allFaces
    cdef list removeTouchingTetra(self,Tetra.Tetrahedron tetrahe,list badTetra,list triangulation,(double,double,double,long int )point): #rozdzielanie ostrosłupów 
        cdef list myVert
        cdef list allfaces
        cdef list sharedWithOtherFaces
        cdef int firstIterator
        cdef int notSharedIterator
        myVert=tetrahe.vertecies #wierzchołki aktulanego ostrosłupa
        allfaces= [{myVert[0],myVert[1],myVert[2]},{myVert[0],myVert[1],myVert[3]},{myVert[3],myVert[1],myVert[2]},{myVert[0],myVert[3],myVert[2]}] #ściany aktualnego ostrosłupa, szybsze niż użycie itertools
        sharedWithOtherFaces=[]
        for firstIterator in range(0,len(badTetra)): #dla każdego ostrosłupa sprawdzane jest czy styka się z pozostałymi, dla tych które się nie stykają genenrowany jest nowy ostrosłup ze ściany oraz nowego punktu
            if len(allfaces)>0: 
                allfaces=self.removeSharedFace(myVert,badTetra[firstIterator].vertecies,allfaces)               
        for notSharedIterator in range(0,len(allfaces)):
            first, second,third = allfaces[notSharedIterator]
            triangulation.append(Tetra.Tetrahedron(first,second,third,point))# generacja nowego ostrosłupa
        triangulation.remove(tetrahe)
        return triangulation
    cdef Tetra.Tetrahedron createSuperTetra(self,double length): #generacja początkowego ostrosłupa zawierającego wszystkie punkty, wielkości boków zostały dobrane empirycznie
        cdef (double,double,double,long int) A
        cdef (double,double,double,long int) B
        cdef (double,double,double,long int) C
        cdef (double,double,double,long int) D
        A=(-3*length,0,-100*2*length,0)
        B=(3*length/sqrt(2),3*length/sqrt(2),-100*2*length,1)
        C=(3*length/sqrt(2),-3*length/sqrt(2),-100*2*length,2)
        D=(0,0,100*2*length,3)
        return Tetra.Tetrahedron(A,B,C,D)
    cdef bint liesOnSuper(self,list vert): #sprawdzane jest czy ostrosłup zawiera conajmniej ścianę super ostrosłupa
        return len(np.intersect1d(vert, self.superTetra.vertecies))>2
    cdef list computeTrianglePoints(self):
        cdef list triangulation
        cdef list filteredTriangulation
        cdef double totalStartTime
        cdef double firstTime
        cdef double secondTime
        cdef double firstT
        cdef double firstET
        cdef double totalEndTime
        cdef double totTime
        
        cdef long int idx 
        cdef list badTetra
        cdef Tetra.Tetrahedron tetrahe
        cdef long int tetraheIdx
        cdef long int iterator
        triangulation=[] 
        triangulation.append(self.superTetra) #początkowo dodawany jest super ostrosłup do zbioru triangulacyjnego
        totalStartTime=time.time()
        firstTime=0
        secondTime=0
        for idx in range(0,len(self.pointSet)):
            if idx%100==0:
                self.updateProcess(idx*100/len(self.pointSet),"Tworzenie triangulacji Delaunay'a")
                print('Procent ukonczenia ',idx*100/len(self.pointSet),'%')
            firstT=time.time()
            badTetra=[]
            
            for iterator in range(0,len(triangulation)):
                if self.calcDistance(triangulation[iterator].O,self.pointSet[idx])<triangulation[iterator].R: #sprawdzae jest czy punkt leży wewnątrz ostrosłupa triangulacyjnego
                    badTetra.append(triangulation[iterator])#jeśli tak to jest on dodawany do tych co powinny zostać przekształcone
            firstET=time.time()
            firstTime+=(firstET-firstT)
            firstT=time.time()
            for tetrahe in badTetra: 
                triangulation=self.removeTouchingTetra(tetrahe,badTetra,triangulation,self.pointSet[idx]) #z tych ostrosłupów tworzymy nowe zawierające punkt triangulacyjny oraz pozostałe dostępne ściany
            firstET=time.time()
            secondTime+=firstET-firstT
        totalEndTime=time.time()
        totTime=totalEndTime-totalStartTime
        print('totaj time',totTime,'first time percentage',firstTime*100/totTime,'%',"second time ",secondTime*100/totTime,'%')

                
            
        filteredTriangulation=[]
        for tetrahe in triangulation:
            if not self.liesOnSuper(tetrahe.vertecies): #usuwane są te, które leżą na super ostrosłupie
                filteredTriangulation.append(tetrahe)

        
        return filteredTriangulation
    cdef  double calcDistance(self,( double, double, double) A,( double, double, double,long int) B):# obliczanie odległośći dwóch punktów od siebie
        cdef double calculated
        cdef double suma
        suma=sqrt( pow(A[0]-B[0],2)+pow(A[1]-B[1],2)+pow(A[2]-B[2],2) ) 
        return suma
    cdef set compareTetraFaces(self,list vertA,list vertB): #sprawdzane jest, czy wierzchołki dwóch ostrosłópów tworzą ścianę
        cdef set face
        face=set(vertB).intersection(set(vertA)) 
        return face

    cdef list transformToIndexes(self): #zamiana wierzchołków ostrosłupa, na odpowiadające im indeksy w początkowym zbiorze
        #adding indexes instead of values
        cdef list verticiesIndex
        cdef Tetra.Tetrahedron tetra
        cdef list tetraTuple
        cdef list newRow
        cdef long int idx
        cdef long int indx
        cdef (double,double,double) xyz
        cdef (double,double,double) tup
        verticiesIndex=[]
        for tetra in self.tetraPoints: # w celu optymalizacji dodano jako dodatkowy parametr w macierzy ich indeks
            newRow=[ tetra.A[3],tetra.B[3],tetra.C[3],tetra.D[3]]
            verticiesIndex.append(newRow)
        return verticiesIndex

    cdef list computeVertexCoordsFacesColors(self): # funkcja służąca do wizualizacji procesu triangulacji Delaunay'a
        cdef list xyz
        cdef list faces
        cdef list colors
        cdef list vert
        cdef list vertexComb
        
        cdef long int index
        cdef (long int,long int,long int) p
        cdef (double,double,double,long int) myPt
        cdef (int,int,int) myFaceColor

        xyz=[]
        faces=[]
        colors=[]
        for vert in self.transformed: #indeksy zamieniane są z powrotem na punkty, by sprawdzić poprawność obliczeń
            for index in vert:
                myPt=self.pointSet[index]
                xyz.append([myPt[0],myPt[1],myPt[2]])
            vertexComb=[(vert[0],vert[1],vert[2]),(vert[0],vert[1],vert[3]),(vert[3],vert[1],vert[2]),(vert[0],vert[3],vert[2])] #generacja ścian ostrosłupa
            for p in vertexComb: #adding faces of tetrahedra
                faces.append(p)
            myFaceColor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            colors.append(myFaceColor)#dla lepszej wizualizacji wszystkie ściany ostrosłupa kolorowane są na ten sam kolor
            colors.append(myFaceColor)
            colors.append(myFaceColor)
            colors.append(myFaceColor)
        total=[xyz,faces,colors]
        return total
    cpdef computeVertices(self): # funkcja wejściowa służąca do obróbki wszystkich punktów ora zwrócenie do głównej klasy indeksów wygenerowanych ścian
        self.tetraPoints=self.computeTrianglePoints()
        self.transformed=self.transformToIndexes()  #transform values of points ,to indexes of them in main point set
        return self.transformed,self.tetraPoints

        




