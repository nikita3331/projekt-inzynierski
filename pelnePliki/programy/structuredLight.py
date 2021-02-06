import numpy as np
import matplotlib.pyplot as plt
from random import randrange
from mpl_toolkits.mplot3d import axes3d, Axes3D
import os
import math
import open3d as o3d
import trimesh
from MyDelaunay import Delaunay



class StructeredLight(): #klasa zajmująca się przetwarzaniem chmur punktów z rs-convert za pomocą metody światła strukturalnego
    def __init__(self,begginingName,directory,minimumHeight,centerDistance,minDistance,maxDistance,firstFrameNumber,numberOfFramesToAquire,PCLVis,bpaVis,delVis,bpaRadius,updateProgress):
        self.begginingName=begginingName
        self.directory=directory
        self.minimumHeight=minimumHeight
        self.centerDistance=centerDistance
        self.minDistance=minDistance
        self.maxDistance=maxDistance
        self.firstFrameNumber=firstFrameNumber
        self.numberOfFramesToAquire=numberOfFramesToAquire
        self.totalNumberOfFrames=len(os.listdir(self.directory))
        self.PCLVis=PCLVis
        self.bpaVis=bpaVis
        self.delVis=delVis
        self.updateProgress=updateProgress
        self.bpaRadius=bpaRadius
    def createAllFromPLY(self): #funkcja uruchumiająca proces generacji 
        loadedPlys=self.loadPlys() #ładowanie klatek
        clearedPcds,pcdCenters=self.clearAllPcds(loadedPlys) #odpowiednia filtracja punktów i danych
        translated=self.translatePcds(clearedPcds,pcdCenters) #przesuwanie by były ustawione względem środka układu współrzędnych
        rotated=self.rotatePcds(translated) #obrót poszczególnych klatek wokół środka układu współrzędnych (osi Y)
        globalyRegistered=self.createGlobalRegistrationForClouds(rotated) #utworzenie rejestracji na podstawie chmur punktów oraz ich zespolenie
        mergedClouds=self.flatenMultipleClouds(globalyRegistered) #połączenie zespolonych chmur punktów
        self.createAndShowResults(mergedClouds) #wyświetlenie wyników

    def loadPlys(self):
        
        allPlys=[]
        upperRange=self.totalNumberOfFrames+self.firstFrameNumber
        step=int(self.totalNumberOfFrames/self.numberOfFramesToAquire) #krok co ile należy wziąć klatkę
        for i in range(0,self.numberOfFramesToAquire):
            self.updateProgress((i+1)*100/self.numberOfFramesToAquire,'Ładowanie chmur') #aktualizacja paska progresu
            fileName = str(self.begginingName)+str(i*step+self.firstFrameNumber)+'.ply' #utworzenie nazwy pliku    

            file_path = os.path.join(self.directory, fileName) #utworzenie ścieżki do pliku
            print('loading file',fileName)
            pcd = o3d.io.read_point_cloud(file_path) #wczytannie danych
            if len(pcd.points)>0: #czasem bywają błędnie załadowane klatki, należy więc to sprawdzić
                allPlys.append(pcd)
        return allPlys
    def clearAllPcds(self,allPcds): #filtracja punktów
        filtered=[]
        centers=[]
        for pcdIndex,pcd in enumerate(allPcds):
            self.updateProgress((pcdIndex+1)*100/len(allPcds),'Filtracja punktów') #aktualizacja paska
            newPoints=[] 
            newColors=[] 
            pcdPoints=np.asarray(pcd.points) #wyznaczenie macierzy współrzędnych i koloru z chmury punktów
            pcdColors=np.asarray(pcd.colors)
            xVals=[]
            for color,point in zip(pcdColors,pcdPoints):
                dist=math.sqrt( point[0]**2+point[1]**2+point[2]**2)
                
                if dist<self.maxDistance and dist>self.minDistance and point[1]>self.minimumHeight:  #sprawdzenie warunków zadanych przez użytkownika
                    newPoints.append(point)
                    newColors.append(color)
                    xVals.append(point[0]) #posłuży do wyznaczenia środka chmury na szerokość
            centers.append([-(max(xVals)+min(xVals))/2,0,self.centerDistance]) #wektor przesunięcia aktualnej chmury do środka układu współrzędnych
            newPcd=o3d.geometry.PointCloud() #konwersja z powrotem na chmurę punktów
            newPcd.points = o3d.utility.Vector3dVector(newPoints)
            newPcd.colors =  o3d.utility.Vector3dVector(newColors)
            filtered.append(newPcd) 
        return filtered,centers
    def translatePcds(self,pcds,centers): #przesunięcie chmury do początku układu współrzędnych
        iterator=0
        for cloud,center in zip(pcds,centers):
            self.updateProgress((iterator+1)*100/len(pcds),'Translacja punktów') #aktualizacja paska progresu
            cloud.translate(center) #przesunięcie
            iterator+=1
        return pcds
    def rotatePcds(self,pcds): #obrót punktów wzdłuż osi Y,
        allAngles=self.createAnglesList(len(pcds)) #utworzenie listy kątów, dla zadanej liczby klatek
        for idx,cloud in enumerate(pcds):
            rotMatrix=np.array([ [math.cos(allAngles[idx]),0,math.sin(allAngles[idx])],[0,1,0],[-math.sin(allAngles[idx]),0,math.cos(allAngles[idx])] ]) #wyznaczenie macierzy obrotu
            cloud.rotate(rotMatrix,False) #obrót
            self.updateProgress((idx+1)*100/len(pcds),'Obracanie punktów') #aktualizacja paska procesu
        return pcds
    def createAnglesList(self,length): #utworzenie listy kątów, dla zadanej liczby klatek
        angles=[]
        for i in range(0,length):
            currAngle=(i)*math.pi*2/length #o jaki kąt ma zostać obrócona chmura względem początkowej
            # currAngle=(length-i)*math.pi*2/length
            angles.append(currAngle)
        return angles
    def createGlobalRegistrationForClouds(self,pcds): #sklejenie wszystkich chmur punktów z ich następnym sąsiadem
        fullNewArr=[]
        initialStarting=pcds[0]
        transSource=0
        transTarget=0
        for idx in range(1,len(pcds)):
            transSource,transTarget=self.globalSourceTarget(initialStarting,pcds[idx]) #przeprowadzenie rejestracji i sklejania
            initialStarting=transTarget
            fullNewArr.append(transSource)
            self.updateProgress((idx)*100/len(pcds),'Sklejanie chmur') #aktualizacja progresu
        transSource,transTarget=self.globalSourceTarget(transTarget,fullNewArr[0]) #ponowne wykonanie dla ostatniej oraz pierwszej chmury punktów
        fullNewArr.append(transSource)
        return fullNewArr
    def globalSourceTarget(self,source,target): #przeprowadzenie globalnej rejestracji oraz sklejenie chmur, przy wykorzystaniu materiałów dydaktycznych biblioteki Open3D
        #http://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html
        def downsamplePoints(pcd, size): #zmniejszenie liczby wierzchołków w celu optymalizacji oraz wyznaczenie histogramu punktów
            pcdDownSampled = pcd.voxel_down_sample(size) #zmniejszenie wierzchołków
            normalSearchRadius = size * 2
            pcdDownSampled.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=normalSearchRadius, max_nn=30)) #estymacja normalnych potrzebna do PFH
            radiusSearchFeature = size * 5 #promień poszukiwań cech geometrii
            pcdFeatures = o3d.registration.compute_fpfh_feature(pcdDownSampled,o3d.geometry.KDTreeSearchParamHybrid(radius=radiusSearchFeature, max_nn=100)) #przeprowadzenie historgramu punktów
            return pcdDownSampled, pcdFeatures
        def downSampleAll(size): # wyznaczenie histogramu punktów oraz zmniejszenie ich liczby dla chmury początkowej oraz docelowej
            sourceDownSampled, sourceFeatures = downsamplePoints(source, size)
            targetDownSampled, targetFeatures = downsamplePoints(target, size)
            return sourceDownSampled, targetDownSampled, sourceFeatures, targetFeatures
        def globalRegisterMerge(sourceD, targetD, sourceFeatures,targetFeatures, size): #przeprowadzenie globalnej rejestracji za pomocą algorytmu RANSAC
            distance_threshold = size * 0.1 
            result = o3d.registration.registration_ransac_based_on_feature_matching(
                sourceD, targetD, sourceFeatures, targetFeatures, distance_threshold,
                o3d.registration.TransformationEstimationPointToPoint(False),
                4, [ #liczba losowo wybranych punktów do ransac
                    o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(
                        0.9), 
                    o3d.registration.CorrespondenceCheckerBasedOnDistance(
                        distance_threshold)#sprawdzenie kryterium odległości cech od siebie
                ], o3d.registration.RANSACConvergenceCriteria(4000000, 500)) #maksymalna ilość iteracji oraz walidacji dla RANSAC
            return result
        size = 0.001  # 1mm odległości od punktów
        sourceDownSampled, targetDownSampled, sourceFeatures, targetFeatures = downSampleAll(size) #zmniejszenie wierzchołków oraz wyznaczenie histogramu punktów
        ransac = globalRegisterMerge(sourceDownSampled, targetDownSampled,sourceFeatures, targetFeatures,size) #przeprowadzenie algorytmu RANSAC
        sourceDownSampled.transform(ransac.transformation)#transformacja początkowej chmury punktów by dopasować do cech docelowej    
        return sourceDownSampled,targetDownSampled
    def flatenMultipleClouds(self,pcds): #połączenie wielu chmur w jedną w celu jej wyświetlenia
        xyz=[]
        myColors=[]
        for idx,cloud in enumerate(pcds): #konwersja wierzchołków z chmur do jednej macierzy
            for point,color in zip(cloud.points,cloud.colors):
                xyz.append(point)
                myColors.append(color)
            self.updateProgress((idx+1)*100/len(pcds),'Tworzenie pojedynczej chmury') #aktualizacja progresu
        mergedCloud=o3d.geometry.PointCloud() #utworzenie PCD z macierzy współrzędnych oraz koloru
        mergedCloud.points = o3d.utility.Vector3dVector(xyz)
        mergedCloud.colors =  o3d.utility.Vector3dVector(myColors)
        
        return mergedCloud
    def showPcd(self,myobj,name):#wyświetlenie wyników
        o3d.visualization.draw_geometries([myobj],window_name=name)
    def createDelaunay(self,pcd): #TUTAJ TO SAMO CO POPRZEDNIO
        xyz=[]
        xyzN=[]
        myColors=[]
        itera=0
        localId=0
        for point,color in zip(pcd.points,pcd.colors):
            xyz.append((point[0]+randrange(-10,10),point[1]+randrange(-10,10),point[2]+randrange(-10,10),localId))
            xyzN.append((point[0]+randrange(-10,10),point[1]+randrange(-10,10),point[2]+randrange(-10,10)))
            myColors.append(color)
            localId+=1
        self.updateProgress(0,"Generacja siatki Delaunay'a dla "+str(len(xyz))+' pkt')
        
        tri = Delaunay(xyz,self.updateProgress)  
        indexes,pts=tri.computeVertices()
        faces=[]
        for vert in indexes:
            vertexComb=[[vert[0],vert[1],vert[2]],[vert[0],vert[1],vert[3]],[vert[3],vert[1],vert[2]],[vert[0],vert[3],vert[2]]] #generacja ścian ostrosłupa
            for p in vertexComb: #adding faces of tetrahedra
                faces.append(p)
        self.updateProgress(100,"Generacja siatki Delaunay'a dla "+str(len(xyz))+' pkt')
        # probnymesh = trimesh.Trimesh(vertices=xyz,faces=faces,vertex_colors=myColors) 
        probnymesh = trimesh.Trimesh(vertices=xyzN,faces=faces,vertex_colors=myColors) 
        probnymesh.export('delauna_structured.ply')
        pcd_load = o3d.io.read_triangle_mesh("delauna_structured.ply")
        return pcd_load
    def createBpa(self,pcd):
        self.updateProgress(0,'Generacja siatki BPA dla '+str(len(pcd.points))+' pkt')#aktualizacja pasku ładowania w GUI,ze względu na brak dostępu do danych wewnątrz BPA, proces aktualizowany jest jako 0 oraz 100
        pcd.estimate_normals()#estymacja normalnych, potrzebna do wyznaczenia algorytmu BPA, opisana bardziej w pracy
        distances = pcd.compute_nearest_neighbor_distance()#wyznaczenie odległości punktów od siebie, pomocne przy doborze promienia kuli
        avg_dist = np.mean(distances)#wyznaczneie średniej odległości sąsiednich punktów
        radius =self.bpaRadius*avg_dist
        bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2] ))#utworzenie BPA za pomocą biblioteki Open3D, dwa promienie oznaczają, że algorytm zostanie wykonany dwa razy dla różnych promieni by polepszyć wynik
        self.updateProgress(100,'Generacja siatki BPA dla '+str(len(pcd.points))+' pkt')# aktualizacja progresu
        tri_mesh = trimesh.Trimesh(np.asarray(bpa_mesh.vertices), np.asarray(bpa_mesh.triangles),vertex_normals=np.asarray(bpa_mesh.vertex_normals),vertex_colors=pcd.colors) #zamiana otrzymanego meshu na postać możliwą do zapisania w pliku .ply
        tri_mesh.export('bpa_structured.ply')
        pcd_load = o3d.io.read_triangle_mesh("bpa_structured.ply")
        return pcd_load
    def createAndShowResults(self,clouds): #wyświetlenie wyników operacji
        if self.bpaVis:
            bpaMesh=self.createBpa(clouds) #przeprowadzenie algorytmu BPA
        if self.delVis:
            delaMesh=self.createDelaunay(clouds) #przeprowadzenie Delaunay'a
        if self.PCLVis:
            o3d.io.write_point_cloud("pointcloud_structured.ply", clouds) #wyświetlenie chmury punktów
            self.showPcd(clouds,"Chmura punktów")
        if self.bpaVis:
            self.showPcd(bpaMesh,"Algorytm BPA") #wyświetlenie BPA
        if self.delVis:
            self.showPcd(delaMesh,"Triangulacja Delaunya'a") #Wyświetlenie Delaunay'a




