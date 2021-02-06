import numpy as np
from scipy.optimize import curve_fit
from scipy import signal

def func(x,a0,a1,a2,a3): #obliczanie współczynników wielomianu 3 stopnia
  y=a0*x**3+a1*x**2+a2**x+a3
  return y

def createLinearizedValues(coeffs,indexes,withoutEmptyIdx,withoutEmptyVals): #generacja nowych wartości na podstawie linearyzacyjnej funkcji
  linearized=[]
  completeArr=np.zeros(len(indexes))
  for itsIndex,itsVal in zip(withoutEmptyIdx,withoutEmptyVals):
    completeArr[itsIndex]=itsVal
  for idx,item in enumerate(completeArr):
    if item==0:
      newItem=func(idx,coeffs[0],coeffs[1],coeffs[2],coeffs[3])
      linearized.append(newItem)
    else:
      linearized.append(item)

  # for i in indexes:
  #   linearized.append(func(i,coeffs[0],coeffs[1],coeffs[2],coeffs[3]))
  return linearized


def mycubic(arr): #utworzoenie linearyzacji 3 stopnia z dostępnych punktów
    indexesWithoutEmpty=[]
    valuesWithoutEmpty=[]
    allIndexes=[]
    
    for idx,item in enumerate(arr):
        if item!=None: #gdy jest równy None, to powinnien być poddany linearyzacji. Jest to sposób na jego oflagowanie
            indexesWithoutEmpty.append(idx) #zbiór tylko określonych wartości
            valuesWithoutEmpty.append(item)
        allIndexes.append(idx) #zbior wszystkich indeksów punktów
    if len(indexesWithoutEmpty)>3: #gdy punktów jest za mało to nie możliwe jest utworzenie odpowiedniej funkcji 3 stopnia  przechodzącej przez nie
        popt, pcov = curve_fit(func, indexesWithoutEmpty, valuesWithoutEmpty) #tworzona jest funkcja przechodząca przez wszystkie punkty
        newVals=createLinearizedValues(popt,allIndexes,indexesWithoutEmpty,valuesWithoutEmpty)#utworzenie nowych wartości na podstawie estymacji
        return newVals
    else:
        return arr



