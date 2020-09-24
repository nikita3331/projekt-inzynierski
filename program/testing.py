import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from random import randrange
import math
import open3d as o3d
import trimesh
from scipy.spatial import Delaunay
from colormap import rgb2hex
import random
def createPoints():
    numberOfPoints=100
    odleglosc=1
    depth=createDepth(numberOfPoints)
    full_x=[]
    full_y=[]
    full_z=[]
    ranges=np.linspace(0,2*math.pi,np.shape(depth)[0])
    for idx,angle in enumerate(ranges):
        d_0=depth[idx]
        xs = np.array([np.cos(angle)*(odleglosc-d_0[numberOfPoints-1-i]) for i in range(0,numberOfPoints)])#wspolrzedne do rysowania
        ys = np.array([np.sin(angle)*(odleglosc-d_0[numberOfPoints-1-i]) for i in range(0,numberOfPoints)])#wspolrzedne do rysowania
        zs=np.linspace(0, 1  ,numberOfPoints)
        full_x.append(xs)
        full_y.append(ys)
        full_z.append(zs)
    return full_x,full_y,full_z



# def createDepth(numberOfPointsInLine):
#     depthArray=[]
#     for i in range(0,1000):
#         row=[]
#         angles=np.linspace(0,4*math.pi,numberOfPointsInLine)
#         for i in angles:
#             row.append(10*np.sin(i))
#         depthArray.append(row)
#     return depthArray
def createDepth(numberOfPointsInLine):
    depthArray=[]
    angles=np.linspace(0,6*math.pi,1000)
    for angle in angles:
        distance=math.sin(angle)
        row=[distance]*numberOfPointsInLine
        depthArray.append(row)
    return depthArray
def showDiagram(x,y,z,color):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x,y,z,c=color)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
def flatCoords(x,y,z):
    fullArr=[]
    colors=[]
    colorspace=np.linspace(0,1,np.shape(x)[0])
    i=0
    for (rowx, rowy, rowz) in zip(x, y, z):
        rowColor=[colorspace[i],0,0]
        for (it_x, it_y, it_z) in zip(rowx, rowy, rowz):  
            fullArr.append([it_x, it_y, it_z] )
            colors.append(rowColor)
        i=i+1
    return fullArr,colors
def createDelaunayMesh(flat,color):
    # tri = Delaunay(flat)
    # faces=[]
    # for i in tri.simplices:
    #     faces.append([i[0],i[1],i[2]])
    # probnymesh = trimesh.Trimesh(vertices=flat,faces=faces,vertex_colors=color)
    # probnymesh.export('testDelaunayMesh.ply')
    # pcd_load = o3d.io.read_triangle_mesh("testDelaunayMesh.ply")
    # o3d.visualization.draw_geometries([pcd_load],window_name='delaunay')

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(flat)
    pcd.colors =  o3d.utility.Vector3dVector(color)
    # o3d.visualization.draw_geometries([pcd],window_name='point cloud')

    pcd.estimate_normals()
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius =15*avg_dist
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2] ))
    tri_mesh = trimesh.Trimesh(np.asarray(bpa_mesh.vertices), np.asarray(bpa_mesh.triangles),vertex_normals=np.asarray(bpa_mesh.vertex_normals),vertex_colors=pcd.colors)
    tri_mesh.export('testbpamesh.ply')
    pcd_load = o3d.io.read_triangle_mesh("testbpamesh.ply")
    o3d.visualization.draw_geometries([pcd_load],window_name='bpa cloud')


    

x,y,z=createPoints()
flat,color=flatCoords(x,y,z)
showDiagram(x,y,z,color)
createDelaunayMesh(flat,color)
