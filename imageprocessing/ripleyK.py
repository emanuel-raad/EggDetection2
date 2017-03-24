import numpy
import math
import matplotlib.pyplot as plt

from pixelDistance import distanceBetweenPointsPixel
from random import randint

def ripleyKFunction(n, coords, area, startD, stopD, incrementD, ripleyMode = 'ripleysK'):
    d = numpy.zeros((n, n), dtype=object)

    # Calculate distance between each combination of points and stores them in an array to access later
    for i in range(0, n-1):
        for j in range(1, n):
            if (j != i):
                # Calculate distance here
                d[i][j] = distanceBetweenPointsPixel(coords[i][0], coords[i][1], coords[j][0], coords[j][1])

    counter = 0
    numIncrement = int((stopD-startD)/incrementD) + 1

    k = numpy.zeros((numIncrement, 2))
    k_scale = numpy.zeros((numIncrement, 2))
    k_l = numpy.zeros((numIncrement, 2))

    ripleysCoeff = (n/area)*n
    ripleysLCoeff = math.sqrt(area/(math.pi*n*(n-1)))

    print "coeff: "+ str(ripleysLCoeff)

    # http://resources.esri.com/help/9.3/arcgisdesktop/com/gp_toolref/spatial_statistics_tools/how_multi_distance_spatial_cluster_analysis_colon_ripley_s_k_function_spatial_statistics_works.htm

    for s in range(startD, stopD+incrementD, incrementD):
        indicator = 0
        for i in range(0, n):
            for j in range(0, n):
                if (j != i):
                    if (i>j):
                        distance = d[j][i]
                    else:
                        distance = d[i][j]
                    # print("{}{}        {}").format(i, j, distance)
                    # print("i {} j {}\tChecking {}<{}").format(i, j, distance, s)
                    if (distance<s):
                        indicator+=1

        ripleys = indicator/ripleysCoeff
        ripleysScale = ripleys - math.pi * math.pow(s, 2)
        k[counter] = [s, ripleys]
        k_scale[counter] = [s, ripleysScale]
        ripleysL = ripleysLCoeff * math.sqrt(indicator)
        k_l[counter] = [s, ripleysL]

        counter += 1

    if ripleyMode == "ripleysK":
        return k
    elif ripleyMode == "ripleysL":
        return k_l
    elif ripleyMode == "ripleysScaleInvariant":
        return k_scale

def main():
    size = 200
    nCoords = 200
    coords = numpy.empty([size, 2])

    # Two clusters
    for i in range(0, nCoords):
        if (i<100):
            coords[i] = [randint(150, 200), randint(150, 200)]
        elif ((i>=100) and (i<=150)):
            coords[i] = [randint(100, 120), randint(100, 120)]
        else:
            coords[i] = [randint(0, 200), randint(0, 200)]

    """
    # Random distribution
    for i in range(0, nCoords):
        coords[i] = [randint(0, 200), randint(0, 200)]
    """

    n = len(coords)
    area = float(size * size)
    r = ripleyKFunction(nCoords, coords, area, 0, size, 2, ripleyMode="ripleysL")

    plt.subplot(121)
    plt.xlim([0, size])
    plt.ylim([0, size])
    plt.scatter(coords[:,0], coords[:,1])
    plt.subplot(122)
    plt.scatter(r[:,0], r[:,1])
    plt.show()

if __name__ == "__main__":
    main()