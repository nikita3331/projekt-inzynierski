import numpy as np
class Point():# klasa przechowująca współrzędne w postaci obiektu
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def toArr(self):#zamiana zmiennych klasy do biblioteki numpy
        return  np.array([self.x,self.y,self.z])
    def toTuple(self):# zamiana zmiennych klasowych do tupla
        return  (self.x,self.y,self.z)

        
        
        
