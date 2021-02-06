import numpy as np
import math
import open3d as o3d
import trimesh
from read3d import loadColorDepth
from linearizePoints import mycubic
from MyDelaunay import Delaunay
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.pyplot as plt
from random import randrange

class LinearScanner(): #klasa obsługująca generację meshu na podstawie kolumn głębi z pliku .bag
    def __init__(self,topLeft,bottomRight,fileDirectory,distanceToCenter,showPcl,showBpa,showDelaunay,bpaRadius,fps,updateProgress):
        #parametrami tej funkcji są wartości podane przez GUI
        self.topLeft=topLeft
        self.bottomRight=bottomRight
        self.fileDirectory=fileDirectory
        self.distanceToCenter=distanceToCenter
        self.showPcl=showPcl
        self.showBpa=showBpa
        self.showDelaunay=showDelaunay
        self.bpaRadius=bpaRadius
        self.depth=None
        self.color=None
        self.oldPath=fileDirectory
        self.fps=fps
        self.updateProgress=updateProgress
    def updateVals(self,topLeft,bottomRight,fileDirectory,distanceToCenter,showPcl,showBpa,showDelaunay,bpaRadius,fps): #funkcja służąca do aktualizacji danych, na przykład po ponownym naciśnięciu przycisku w programie
        self.topLeft=topLeft
        self.bottomRight=bottomRight
        self.fileDirectory=fileDirectory
        self.distanceToCenter=distanceToCenter
        self.showPcl=showPcl
        self.showBpa=showBpa
        self.showDelaunay=showDelaunay
        self.bpaRadius=bpaRadius
        self.fps=fps
    def createFromVideo(self):
        if not self.depth or self.oldPath!=self.fileDirectory: #sprawdzany jest warunek czy trzeba ponownie ładować plik wideo
            self.oldPath=self.fileDirectory
            self.depth,self.color=loadColorDepth(self.topLeft,self.bottomRight,self.fileDirectory,self.fps,self.updateProgress,self.distanceToCenter) #poszczególne kolumny są ładowane z pliku
        xyz,colors=self.create3DPoints(self.color,self.depth)#konwersja danych głębi do chmury obróconych punktów
        myPcd=self.createPcd(xyz,colors) #konwersja macierzy punktów w postaci współrzędnych i kolorów do chmury obsługiwanej przez Open3D
        self.createAndShowResults(myPcd,xyz,colors)
    def createAndShowResults(self,cloud,xyz,colors):#funkcja odpowiedzialna za wyświetlanie oraz zapis wyników obróbki danych
        if self.showBpa:
            bpaMesh=self.createBpa(cloud) #funkcja tworząca BPA
        if self.showDelaunay:
            delaunayMesh=self.createDelaunay(xyz,colors) #funkcja tworząca triangulację Delaunay'a
        if self.showPcl:
            self.showPcd(cloud,"Chmura punktów skaner liniowy") #wyświetlenie PCD
        if self.showBpa:
            self.showPcd(bpaMesh,"Algorytm BPA skaner liniowy") #wyświetlenie BPA
        if self.showDelaunay:
            self.showPcd(delaunayMesh,"Triangulacja Delauny'a skaner liniowy") #wyświetlenie Delaunay'a
    def calcHeightFromPixel(self,distance,height): #funkcja wyznaczająca rzeczywistą wysokość przedmiotu na podstawie jego wysokośći w px. Dokładniej opisane w pracy.
        objHeight=(distance*height*42.5*math.pi/180)/309
        return objHeight
    def meanPointDistance(self,depth,angles): #wyznaczneie średniej odległości punktów od środka układu współrzędnych. Pod uwage brane są tylko współrzędne X oraz Y, ze względu na sposób generacji danych
        totalSum=0
        iterator=0
        punkty_w_linii=np.shape(depth)[1]
        for angle,d_0 in zip(angles,depth):
            xs = np.array([np.cos(angle)*(self.distanceToCenter-d_0[punkty_w_linii-1-i]) for i in range(0,punkty_w_linii)])#wspolrzedne do rysowania
            ys = np.array([np.sin(angle)*(self.distanceToCenter-d_0[punkty_w_linii-1-i]) for i in range(0,punkty_w_linii)])#wspolrzedne do rysowania
            for x,y in zip(xs,ys):
                totalSum+=math.sqrt(x**2+y**2)
                iterator+=1
        totalSum=totalSum/iterator
        return totalSum
    def filterAndLinearize(self,xs,ys,procent,meanDistance): #Usunięcie punktów w zlej odległości od środka. Potrzebny jest odpowiedni dobór współczynnika
        xs_kopia=[]
        ys_kopia=[]
        for x,y in zip(xs,ys):
            if math.sqrt(x**2+y**2)>procent*meanDistance: #jeśli są za daleko to są oflagowane
                xs_kopia.append(None)
                ys_kopia.append(None)
            else:
                xs_kopia.append(x)
                ys_kopia.append(y)
        xs_lin=mycubic(xs_kopia) #wszystkie są poddane linearyzacji, by naprawić te oflagowane
        ys_lin=mycubic(ys_kopia)
        return xs_lin,ys_lin
    def clearWrongPointsAndVectorize(self,xs,ys,zs,colors): #robimy je plaskimi oraz usuwamy te odstajace od normy (te ktore sa rowne None)
        clearedColors=[]
        clearedXYZ=[]
        for x_row,y_row,z_row,c_row in zip(xs,ys,zs,colors):
            for x,y,z,c in zip(x_row,y_row,z_row,c_row):
                if x!=None and y!=None: #jezeli jeszcze któreś zostały po linearyzacji
                    clearedXYZ.append([x,y,z])
                    clearedColors.append(c)
        return clearedXYZ,clearedColors
    def create3DPoints(self,colors,depth): #główna funkcja do generacji chmury punktów na podstawie danych o głębi kolumn
        
        skalowanie=100
        numPointsInColumn=np.shape(depth)[1]
        initialDistanceFromObj=depth[0][int(numPointsInColumn/2)] #wyznaczenie środka obiektu oraz odległości od niego
        objHeight=self.calcHeightFromPixel(initialDistanceFromObj,numPointsInColumn)
        xs_ful=[]
        ys_ful=[]
        zs_ful=[]
        rgb_ful=[]
        angles=np.linspace( math.pi*2, 0  ,np.shape(depth)[0])

        errorPercentage=1.7 #współczynnik odległości punktów od środka układu współrzędnych, np. 170%
        meanDistance=self.meanPointDistance(depth,angles)
        iterator=1
        print('liczba kolumn',np.shape(depth)[0],' w kolumnie',numPointsInColumn)
        for angle,d_0,colo in zip(angles,depth,colors):
            self.updateProgress(iterator*100/np.shape(depth)[0],'Przetwarzanie kolumn') #aktualizacja pasku ładowania w GUI
            zs=np.linspace(0, objHeight  ,numPointsInColumn) #wysokość jest równomiernie rozłożona wzdłuż całej osi
            xs = np.array([np.cos(angle)*(self.distanceToCenter-d_0[numPointsInColumn-1-i]) for i in range(0,numPointsInColumn)])#wspolrzedne X punktów w kolumnie
            ys = np.array([np.sin(angle)*(self.distanceToCenter-d_0[numPointsInColumn-1-i]) for i in range(0,numPointsInColumn)])#wspolrzedne Y punktów w kolumnie
            rgbColorColumn=np.array([[pix[0]/255,pix[1]/255,pix[2]/255] for pix in colo])#skalowanie kolorów pikseli
            xs,ys=self.filterAndLinearize(xs,ys,errorPercentage,meanDistance) #filtracja i linearyzacja błędnych punktów
            #dodanie kolumn do całego zbioru
            zs_ful.append(zs)
            ys_ful.append(ys)
            xs_ful.append(xs)
            rgb_ful.append(rgbColorColumn)
            iterator+=1
        xyz,colors=self.clearWrongPointsAndVectorize(xs_ful,ys_ful,zs_ful,rgb_ful) #by stworzyć płaskie macierze i usunąć pozostałości po linearyzacji
        return xyz,colors
    def createBpa(self,pcd):
        self.updateProgress(0,'Generacja siatki BPA') #aktualizacja pasku ładowania w GUI,ze względu na brak dostępu do danych wewnątrz BPA, proces aktualizowany jest jako 0 oraz 100
        pcd.estimate_normals() #estymacja normalnych, potrzebna do wyznaczenia algorytmu BPA, opisana bardziej w pracy
        distances = pcd.compute_nearest_neighbor_distance() #wyznaczenie odległości punktów od siebie, pomocne przy doborze promienia kuli
        avg_dist = np.mean(distances) #wyznaczneie średniej odległości sąsiednich punktów
        radius =self.bpaRadius*avg_dist
        bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2] )) #utworzenie BPA za pomocą biblioteki Open3D, dwa promienie oznaczają, że algorytm zostanie wykonany dwa razy dla różnych promieni by polepszyć wynik
        tri_mesh = trimesh.Trimesh(np.asarray(bpa_mesh.vertices), np.asarray(bpa_mesh.triangles),vertex_normals=np.asarray(bpa_mesh.vertex_normals),vertex_colors=pcd.colors) #zamiana otrzymanego meshu na postać możliwą do zapisania w pliku .ply
        tri_mesh.export('bpa_linear.ply')
        pcd_load = o3d.io.read_triangle_mesh("bpa_linear.ply")
        self.updateProgress(100,'Generacja siatki BPA')# aktualizacja progresu
        return pcd_load
    def createDelaunay(self,xyz,colors): #generacja Delaunay'a autorską metodą
        xyzWithIndex=[]

        xs=[]
        ys=[]
        zs=[]
        newaColors=[]
        xyzWithoutIndex=[]
        itera=0
        localId=0
        numbersRandX=np.random.uniform(low=-0.001, high=0.001, size=len(xyz))
        numbersRandY=np.random.uniform(low=-0.001, high=0.001, size=len(xyz))
        numbersRandZ=np.random.uniform(low=-0.001, high=0.001, size=len(xyz))
        for idx,point in enumerate(xyz): #zamiana punktów na odpowiedni format, dopisanie ich indeksu w celu zwiększenia wydajności
            if itera%2==0:
                xyzWithIndex.append((point[0]+numbersRandX[localId],point[1]+numbersRandY[localId],point[2]+numbersRandZ[localId],localId))
                xyzWithoutIndex.append([point[0]+numbersRandX[localId],point[1]+numbersRandY[localId],point[2]+numbersRandZ[localId]])
                newaColors.append(colors[itera])
                localId+=1
            itera+=1

        myDelObj = Delaunay(xyzWithIndex,self.updateProgress)
        # myDelObj = []
        indexes,pts=myDelObj.computeVertices() #wyznaczenie indeksów wierzchołków trójkątów
        faces=[]
        for vert in indexes: #zamiana na indeksy
            vertexComb=[[vert[0],vert[1],vert[2]],[vert[0],vert[1],vert[3]],[vert[3],vert[1],vert[2]],[vert[0],vert[3],vert[2]]] #generacja ścian ostrosłupa
            for p in vertexComb: #
                faces.append(p)
        probnymesh = trimesh.Trimesh(vertices=xyzWithoutIndex,faces=faces,vertex_colors=newaColors)#zapis do pliku 
        probnymesh.export('delaunay_linear.ply')
        pcd_load = o3d.io.read_triangle_mesh("delaunay_linear.ply")
        return pcd_load
    def createPcd(self,xyz,colors): #konwersja macierzy współrzędnych oraz kolorów do chmury punktów
        self.updateProgress(0,'Generacja chmury punktów')
        pcd=o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.colors =  o3d.utility.Vector3dVector(colors)
        o3d.io.write_point_cloud("pointcloud_linear.ply", pcd)
        self.updateProgress(100,'Generacja chmury punktów')
        return pcd
    def showPcd(self,myobj,name): #wyświetlenie wyników operacji, np. BPA, PCD lub Delaunay
        o3d.visualization.draw_geometries([myobj],window_name=name)


