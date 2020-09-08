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
def laduj_klatki_glebia(kolumna,wiersz_gora,wiersz_dol,nazwa,liczba_klatek):
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config,nazwa)
    config.enable_stream(rs.stream.depth , 848, 480, rs.format.z16, 6) #wczesniej nie bylo komentowane
    sta=pipeline.start(config)
    #sta.get_device().as_playback().set_real_time(False)

    l_klatek=0 
    kolumny=[]
    kolory=[]
    for l_klatek in range(0,liczba_klatek):
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        kolumna_cala=[]
        kolumna_kolor_cala=[]

        
        for i in range(wiersz_gora,wiersz_dol+1):
            zDepth = depth_frame.get_distance(int(kolumna),int(i))
            kolumna_cala.append(zDepth)

        kolumny.append(kolumna_cala)
        os.system('cls')
        print('ladujemy glebie',(l_klatek/liczba_klatek)*100,' %')
    pipeline.stop()
    return kolumny
def laduj_klatki_kolor(kolumna,wiersz_gora,wiersz_dol,nazwa,liczba_klatek):
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config,nazwa)
    config.enable_stream(rs.stream.color , 848, 480, rs.format.rgb8, 6)
    sta=pipeline.start(config)
    #sta.get_device().as_playback().set_real_time(False)


    l_klatek=0 
    kolumny=[]
    kolory=[]
    for l_klatek in range(0,liczba_klatek):
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image_n = np.asanyarray(color_frame.get_data())
        
        kolumna_cala=[]
        kolumna_kolor_cala=[]

        
        for i in range(wiersz_gora,wiersz_dol+1):
            kolumna_kolor_cala.append(color_image_n[int(kolumna),int(i)])

        kolory.append(kolumna_kolor_cala)
        os.system('cls')
        print('ladujemy kolor',(l_klatek/liczba_klatek)*100,' %')
    pipeline.stop()
    return kolory