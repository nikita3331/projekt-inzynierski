import numpy as np
import matplotlib.pyplot as plt
from random import randrange
from mpl_toolkits.mplot3d import axes3d, Axes3D
import pyrealsense2 as rs
import cv2
import os
import pprint
import math
import open3d as o3d
import trimesh
import pandas as pd
from depend.read3d import laduj_klatki_glebia,laduj_klatki_kolor
from scipy.spatial import Delaunay
os.chdir('C:/Users/Nikita/Desktop/inzynierka')

def licz_srednia_odleglosc(glebia,zakres,odleglosc,skalowanie):
    srednia=0
    iterator=0
    punkty_w_linii=np.shape(glebia)[1]
    for idx,angle in enumerate(zakres):
        
        d_0=glebia[idx]


        xs = np.array([skalowanie*np.cos(angle)*(odleglosc-d_0[punkty_w_linii-1-i]) for i in range(0,punkty_w_linii)])#wspolrzedne do rysowania
        ys = np.array([skalowanie*np.sin(angle)*(odleglosc-d_0[punkty_w_linii-1-i]) for i in range(0,punkty_w_linii)])#wspolrzedne do rysowania

        for idx,j in enumerate(xs):
            srednia+=math.sqrt(j**2+ys[idx]**2)
            iterator+=1
    srednia=srednia/iterator
    return srednia

def normalizuj(xs,ys,procent,srednia_odleglosc): #if point distance is greater than percantage,remove this point
    xs_kopia=xs.copy()
    ys_kopia=ys.copy()
    for idx,j in enumerate(xs):
        if math.sqrt(j**2+ys[idx]**2)>(1+procent/100)*srednia_odleglosc:
            xs_kopia[idx]=0
            ys_kopia[idx]=0
    return xs_kopia,ys_kopia
def stworz_plaskie_kolory(przetworzone_moje_kolory):
    flat_list_moja=[]
    for sublist in przetworzone_moje_kolory:
        for item in sublist:
            #flat_list_moja.append(item)
            flat_list_moja.insert(0, item)
    return flat_list_moja
def wyswietl_wykresy(xs,ys,zs,kolory):
    fig = plt.figure()
    ax = Axes3D(fig)
    
    ax.scatter(xs,ys,zs,c=kolory)
    #ax.plot_wireframe(np.array(xs), np.array(ys), np.array(zs))

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
def wyczysc_punkty(xs,ys,zs,kolory,kolory_rgb): #robimy je plaskimi oraz usuwamy te odstajace od normy (te ktore sa rowne 0)
    
    liczba_kolumn=np.shape(xs)[1]
    nowe_kolory=[]
    nowe_kolory_rgb=[]
    nowe_xs=[]
    nowe_ys=[]
    nowe_zs=[]
    for i,sublist in enumerate(xs):#jestesmy w wierszu
        for j,item in enumerate(sublist):#jestesmy w kolumnie
            if item!=0:
                nowe_xs.append(item)
                nowe_ys.append(ys[i][j])
                nowe_zs.append(zs[i][j])
                nowe_kolory.append(kolory[i*liczba_kolumn+j])
                nowe_kolory_rgb.append(kolory_rgb[i*liczba_kolumn+j])
            else:
                print(j)
    return nowe_xs,nowe_ys,nowe_zs,nowe_kolory,nowe_kolory_rgb
def stworz_zbior(kolory_wczytane,glebia,liczba_max_klatek,odleglosc,odleglosc_od_obiektywu,wyswiet_wykres):
    wysokosc=0.05
    wysokosc=0.113*np.shape(glebia)[1]/(0.1636/(0.0037*odleglosc_od_obiektywu)-10.634)
    skalowanie=100
    punkty_w_linii=np.shape(glebia)[1]
    xs_ful=[]
    ys_ful=[]
    zs_ful=[]
    przetworzone_moje_kolory=[]
    przetworzone_moje_kolory_rgb=[]
    biore=liczba_max_klatek #tutaj mozna ustawic ile ich chcemy wziac
    zak=np.linspace(0, math.pi*2*biore/liczba_max_klatek  ,np.shape(glebia)[0])

    procent_bledu=45 #musi byc wiecej niz pierwiastek z dwoch

    #policzmy srednia odleglosc punktow
    srednia_odleglosc=licz_srednia_odleglosc(glebia,zak,odleglosc,skalowanie)


    for idx,angle in enumerate(zak):
        
        d_0=glebia[idx]

        zs=np.linspace(0, wysokosc*skalowanie  ,punkty_w_linii)

        xs = np.array([skalowanie*np.cos(angle)*(odleglosc-d_0[punkty_w_linii-1-i]) for i in range(0,punkty_w_linii)])#wspolrzedne do rysowania
        ys = np.array([skalowanie*np.sin(angle)*(odleglosc-d_0[punkty_w_linii-1-i]) for i in range(0,punkty_w_linii)])#wspolrzedne do rysowania
        xs,ys=normalizuj(xs,ys,procent_bledu,srednia_odleglosc)
        


        zs_ful.append(zs)
        ys_ful.append(ys)
        xs_ful.append(xs)

        kolor_linii_mojej = []
        kolor_linii_mojej_rgb=[]
        kolor_linii_mojej_test = []
        for kolumna in range(0,punkty_w_linii):
            pixel=kolory_wczytane[ idx][kolumna ]
            skalowany_pixel=[pixel[0]/255,pixel[1]/255,pixel[2]/255]
            szary=float( ((0.3 * pixel[0]) + (0.59 * pixel[1]) + (0.11 * pixel[2]))/255.0)
            kolor_hex=rgb2hex(pixel[0],pixel[1],pixel[2])
            kolor_linii_mojej.append(kolor_hex)
            kolor_linii_mojej_rgb.append(skalowany_pixel)
        przetworzone_moje_kolory.append(np.array(kolor_linii_mojej) )
        przetworzone_moje_kolory_rgb.append(np.array(kolor_linii_mojej_rgb) )


    plaskie_kolory=stworz_plaskie_kolory(przetworzone_moje_kolory)
    plaskie_kolory_rgb=stworz_plaskie_kolory(przetworzone_moje_kolory_rgb)


    nowe_x,nowe_y,nowe_z,nowe_kolory,kolory_rgb=wyczysc_punkty(xs_ful,ys_ful,zs_ful,plaskie_kolory,plaskie_kolory_rgb)
    if wyswiet_wykres:
        wyswietl_wykresy(nowe_x,nowe_y,nowe_z,nowe_kolory)
    return nowe_x,nowe_y,nowe_z,nowe_kolory,kolory_rgb

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)
def start(zapisany,zapisz_point_cloud,wyswiet_wykres,odleglosc_od_obiek):
    if not plik_zapisany: 
        glebia=laduj_klatki_glebia(kolumna,lewy_gorny[1],prawy_dolny[1],nazwa,ilosc_moich_klatek)
        kolor=laduj_klatki_kolor(kolumna,lewy_gorny[1],prawy_dolny[1],nazwa,ilosc_moich_klatek)
        np.save('24062020save_depth.npy', glebia)
        np.save('24062020save_color.npy', kolor)
        print('zapisalismy klatki do NPY')
        xs,yz,zs,kolory,kolory_rgb=stworz_zbior(kolor,glebia,ilosc_moich_klatek,odleglosc_kamery,odleglosc_od_obiek,wyswiet_wykres)
        if zapisz_point_cloud:
            exportModels(xs,yz,zs,kolory_rgb)
    else:
        glebia = np.load('24062020save_depth.npy')
        kolor = np.load('24062020save_color.npy')
        print('wczytalismy klatki z NPY')
        xs,yz,zs,kolory,kolory_rgb=stworz_zbior(kolor,glebia,ilosc_moich_klatek,odleglosc_kamery,odleglosc_od_obiek,wyswiet_wykres)
        if zapisz_point_cloud:
            exportModels(xs,yz,zs,kolory_rgb)

def flatCoords(xs,ys,zs):
    xyz=[]
    for idx,item in enumerate(xs):
        subarray=[]
        subarray.append(item)
        subarray.append(ys[idx])
        subarray.append(zs[idx])
        xyz.append(subarray)
    return xyz
def createPointCloudMeshLibrary(colors,xyz):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.colors =  o3d.utility.Vector3dVector(colors)
    resp2=o3d.io.write_point_cloud("punkty_pudelko_240620202_pointcloud.ply", pcd)
    pcd.estimate_normals()
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2] ))
    tri_mesh = trimesh.Trimesh(np.asarray(bpa_mesh.vertices), np.asarray(bpa_mesh.triangles),vertex_normals=np.asarray(bpa_mesh.vertex_normals),vertex_colors=pcd.colors) 
    tri_mesh.export('punkty_pudelko_240620202_mesh.ply')

def exportModels(xs,ys,zs,kolory_rgb):
    xyz=flatCoords(xs,ys,zs)
    
    createPointCloudMeshLibrary(kolory_rgb,xyz)


    tri = Delaunay(xyz)
    faces=[]
    for i in tri.simplices:
        faces.append([i[0],i[1],i[2]])
    probnymesh = trimesh.Trimesh(vertices=xyz,faces=faces,vertex_colors=kolory_rgb) #to jest ok,dziala jak powinno,faces mozemy dac pierwsyz drugi trzeci,pierwsyz drugi trzeci
    probnymesh.export('punkty_pudelko_240620202_delaunay.ply')

    
def readModels():
    pcd_load = o3d.io.read_triangle_mesh("punkty_pudelko_240620202_delaunay.ply")
    o3d.visualization.draw_geometries([pcd_load],window_name='delaunay')
    pcd_load = o3d.io.read_triangle_mesh("punkty_pudelko_240620202_mesh.ply")
    o3d.visualization.draw_geometries([pcd_load],window_name='mesh')
    pcd_load = o3d.io.read_point_cloud("punkty_pudelko_240620202_pointcloud.ply")
    xyz_load = np.asarray(pcd_load.points)
    o3d.visualization.draw_geometries([pcd_load],window_name='pointcloud')
###################konfiguracja 
lewy_gorny=(403,270) #x,y
prawy_dolny=(443,355) #x,y 284
kolumna=int((lewy_gorny[0]+prawy_dolny[0])/2)
ilosc_moich_klatek=348
nazwa='pudelko24062020_0.27m.bag'
odleglosc_kamery=0.27
odleglosc_od_obiek=0.23
###################koniec konfiguracji 

plik_zapisany=True
zapisz_point_cloud=True
wyswiet_wykres=True
start(plik_zapisany,zapisz_point_cloud,wyswiet_wykres,odleglosc_od_obiek)
readModels()
