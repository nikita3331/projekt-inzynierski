import numpy as np
import matplotlib.pyplot as plt
from random import randrange
from mpl_toolkits.mplot3d import axes3d, Axes3D
import pyrealsense2 as rs
import cv2
import os
import math
import open3d as o3d
import trimesh


def slowProc(frames,fullGlebiaNowa,fullColorNowy,clipping_distance,topLeft,bottomRight):
    align_to = rs.stream.color
    align = rs.align(align_to)#nałożenie danych głębi oraz koloru
    aligned_frames = align.process(frames.as_frameset())
    hole_filling = rs.hole_filling_filter()#filtracja by załatać dziury
    spatial = rs.spatial_filter()# wszystkie filtry służą polepszeniu wyglądu nagrania  
    spatial.set_option(rs.option.filter_magnitude, 5) #można je wypróbować w RealSense Viewer
    spatial.set_option(rs.option.filter_smooth_alpha, 1)
    spatial.set_option(rs.option.filter_smooth_delta, 50)  
    spatial.set_option(rs.option.holes_fill, 3)
    aligned_depth_frame = aligned_frames.get_depth_frame() 
    
    #przetworzenie klatek odpowiednimi filtrami
    aligned_depth_frame = hole_filling.process(aligned_depth_frame)
    aligned_depth_frame = spatial.process(aligned_depth_frame)
    aligned_depth_frame = aligned_depth_frame.as_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    color_image_n = np.asanyarray(color_frame.get_data())
    columnNumber=int((topLeft[0]+bottomRight[0])/2)#która kolumna zostanie wybrana




    grey_color = 153 #kolor dla zamiany tła
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    dep=[]
    kolo=[] 
    for p in range(topLeft[1],bottomRight[1]+1): #zebranie kolorów całej kolumny
        kolo.append(color_image_n[p][columnNumber])
    
    for i in range(topLeft[1],bottomRight[1]+1): #zebranie głębi z całej kolumny
        zDepth = aligned_depth_frame.get_distance(int(columnNumber),int(i))
        dep.append(zDepth)
    fullGlebiaNowa.append(dep)
    fullColorNowy.append(kolo)

    depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #nałożenie danych głębi by utworzyć obraz
    bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image_n)# usunięcie tła
    bg_removed = cv2.rectangle(bg_removed, topLeft, bottomRight,(0,255,0), 2) #nałożenie prostokąta ROI w celu wizualizacji wyboru użytkownika
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET) #konwersja danych głębi
    depth_colormap = cv2.rectangle(depth_colormap, topLeft, bottomRight,(0,255,0), 2) #nałożenie prostokątów jest na oba obrazy
    images = np.hstack((bg_removed, depth_colormap))# ułożenie zdjęć obok siebie
    cv2.namedWindow('Obraz nagrania', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Obraz nagrania', images)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()


def loadColorDepth(topLeft,bottomRight,filePath,fps,updateProgress,distanceFromCenter): #główna funkcja służąca do ładowania klatek z pliku .bag
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config,filePath, repeat_playback=False)
    queue = rs.frame_queue(1000, keep_frames=True) #bufor dla klatek, dzięki czemu można wykonywać badziej złożone obliczenia bez utraty klatek    
    profile = pipeline.start(config,queue)
    playback=profile.get_device().as_playback()
    durationSeconds=playback.get_duration().total_seconds() #całkowity czas trwania filmu
    aproximateTotalFrames=int(durationSeconds*fps) # by móc wyznaczyć procent ukończenia ładowania, nie wpływa to jednak na sam proces ładowania
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    

    clipping_distance_in_meters = distanceFromCenter #wyznaczenie odległości do usunięcia tła
    clipping_distance = clipping_distance_in_meters / depth_scale #przeskalowanie odległości

    fullGlebiaNowa=[]
    fullColorNowy=[]
    areFrames=True
    l_klatek=0 
    while areFrames: #proces ładowania i obróbki klatek
        try:    
            frames = queue.wait_for_frame()
        except:
            areFrames=False
        if not frames:
            continue
        if l_klatek%3==0: #można zmniejszyć ilość klatek, wpływa to na czas trwania Delaunay'a
            slowProc(frames,fullGlebiaNowa,fullColorNowy,clipping_distance,topLeft,bottomRight) #przetwarzanie danych
        updateProgress(l_klatek*100/aproximateTotalFrames,'Ładowanie pliku')#aktualizacja pasku postępu w GUI
        os.system('cls')
        l_klatek+=1
    cv2.destroyAllWindows()
    pipeline.stop()
    return fullGlebiaNowa,fullColorNowy
