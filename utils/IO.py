import numpy as np
from numpy import genfromtxt
import csv

def writeToCSV(array, path):
    with open(path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(array)

    f.close()

def readFromCSV(path):
    return genfromtxt(path, delimiter=',')

gps= np.asarray([ [1,2], [4,5], [7,8] ])
writeToCSV(gps, 'gps.csv')
a = readFromCSV('gps.csv')
print a