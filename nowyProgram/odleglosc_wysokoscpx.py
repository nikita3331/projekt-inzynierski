import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin
import math
punkty_y_gorny=np.array([208,214,220,226,230,245,245,250,250,253,255,257])
punkty_y_dolny=np.array([427,413,403,389,375,365,357,347,340,333,328,322])
roznica=punkty_y_dolny -punkty_y_gorny
odleglosci=np.array([0.19,0.215,0.225,0.255,0.295,0.333,0.37,0.4,0.44,0.48,0.53,0.58])

def resp(p1,p2,p3):
    nowa=[]
    for i in odleglosci:
        kwadrat=p1/(p2*(i))+p3
        nowa.append(kwadrat)
    return nowa
def squares(param):
  sqr = 0
  trans=resp(param[0], param[1], param[2])
  for idx,i in enumerate(roznica):
      sqr += (float(i) -trans[idx] )**2
  wynik=math.sqrt(sqr*(1/len(roznica)))
  return wynik
def dopasuj():
  startowa_old=[ 0.1,0.1,6]
  fit=fmin(squares,startowa_old,maxiter=10000)
  return fit

dopy=dopasuj()
wynikowa=resp(dopy[0],dopy[1],dopy[2])
print(dopy)
plt.plot(odleglosci,roznica,odleglosci,wynikowa)
plt.show()
