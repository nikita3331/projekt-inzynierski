# Projekt inżynierski
Celem niniejszej pracy dyplomowej było stworzenie skanera 3D oraz systemu wizualizacji utworzonych modeli rzeczywistych obiektów. Do budowy urządzenia wykorzystano kamerę głębi firmy Intel o nazwie RealSense D435i. W pracy został przedstawiony sposób budowy skanera 3D, jego kalibracji oraz algorytmy służące do przetwarzania otrzymanych danych pomiarowych w celu uzyskania wirtualnych modeli. Dokonano porównania wpływu częstotliwośći próbkowania na ostateczny wygląd modelu. Opracowano dwie metody przekształcenia danych z kamery głębi do postaci trójwymiarowej: 
  - Metodę skanera liniowego
  - Metodę triangulacji laserowej
  
Na chmurze punktów utworzono siatkę przy wykorzystaniu algorytmu BPA oraz autorskiej metody triangulacji Delaunay'a.
W celu łatwiejszej obsługi programu został utworzony interfejs graficzny zawierający najważniejsze parametry wizualizacji i obróbki danych. Na koniec dane są eksportowane do modeli w formacie obsługiwanym przez program Blender.
# Engineer diploma
The purpose of this thesis was to create a 3D scanner and visualization system for the created models of real objects. An Intel depth camera called RealSense D435i was used to build the device. The thesis presents how to build a 3D scanner, its calibration and algorithms used to process the obtained measurement data to obtain virtual models. The influence of sampling frequency on the final appearance of the model was compared. Two methods of transforming data from depth camera to three-dimensional form were developed: 
  - Line scanner method
  - Laser triangulation method
  
A mesh was created on the point cloud using the BPA algorithm and the author's Delaunay triangulation method.
In order to make the program easier to use, a graphical interface has been created containing the most important parameters for visualization and data processing. Finally, the data are exported to models in a format supported by the Blender program.


