import numpy as np
class Point():
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def toArr(self):
        return  np.array([self.x,self.y,self.z])
    def toTuple(self):
        return  (self.x,self.y,self.z)

        
        
        
