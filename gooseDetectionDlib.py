import cv2
import dlib
import glob
import os
import csv
import numpy as np
from utils.timer import Timer
from histogram import querySearch
from imageprocessing.pixelDistance import distanceBetweenPointsPixel
from numpy import genfromtxt
timer = Timer()

# Filename of images to search
path = './img/colors/query/*'
imagePaths = glob.glob(path)
imageNames = [os.path.basename(x) for x in imagePaths]
print imageNames

csvFilePaths = ['./img/colors/csv/locations_green.csv',
                './img/colors/csv/locations_blue.csv',
                './img/colors/csv/locations_red.csv']
species = ['green', 'blue', 'red']

fileGreen = open(csvFilePaths[0], 'wb')
fileBlue = open(csvFilePaths[1], 'wb')
fileRed = open(csvFilePaths[2], 'wb')
writerGreen = csv.writer(fileGreen)
writerBlue = csv.writer(fileBlue)
writerRed = csv.writer(fileRed)

pathToDetector = 'detector_colors.svm'
detector = dlib.simple_object_detector(pathToDetector)
green = (0, 255, 0)

for p in range(len(imagePaths)):
    frame = cv2.imread(imagePaths[p])
    rows, cols = frame.shape[:2]

    dets = detector(frame)
    print("Detections: {}").format(len(dets))

    if len(dets) > 0:
        for i, d in enumerate(dets):
            """
            Create a rectangular region of interest around each detection
            Frame is accessed by pixel [startY:endY, startX:endX]
            """
            roi = frame[d.top():d.bottom(), d.left():d.right()]
            # from d.center() get the GPS position of the goose

            # Test ROI to see what goose species it is
            species = querySearch.search(roi, './histogram/histogramIndexColors')
            species = species[0:species.find('_')]
            # print species

            # rowToWrite = [d.center().x, d.center().y, species]
            # writer.writerow(rowToWrite)
            if species == 'green':
                writerGreen.writerow([d.center().x, d.center().y])
            elif species == 'blue':
                writerBlue.writerow([d.center().x, d.center().y])
            elif species == 'red':
                writerRed.writerow([d.center().x, d.center().y])
            else:
                print "oops"

            roiPath = './img/colors/roi/' + species + '_' + imageNames[p] + '_' + str(i) + '.jpg'
            cv2.imwrite(roiPath, roi)

fileGreen.close()
fileBlue.close()
fileRed.close()

for s in range(len(csvFilePaths)):
    coords = genfromtxt(csvFilePaths[s], delimiter=',')
    print species[s]
    n = len(coords)
    d = np.zeros((n, n), dtype=object)
    for i in range(0, n-1):
        for j in range(1, n):
            if (j != i):
                # Calculate distance here
                d[i][j] = round(distanceBetweenPointsPixel(coords[i][0], coords[i][1], coords[j][0], coords[j][1]), 2)
    print d
    print '\n'

