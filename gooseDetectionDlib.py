import argparse
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

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required = True,
	help = "Path to where the detector is stored")
ap.add_argument("-q", "--queryImages", required = True,
	help = "Path to image to search through")
ap.add_argument("-i", "--histogramIndex", required = True,
	help = "Path to the histogram index")
ap.add_argument("-r", "--pathROI", required = True,
	help = "Path to store the detections")
args = vars(ap.parse_args())

timer = Timer()

# Filename of images to search
path = args["queryImages"]
imagePaths = glob.glob(path)
imageNames = [os.path.basename(x) for x in imagePaths]
print imageNames

csvFilePaths = ['./img/colors/csv/locations_canada.csv',
                './img/colors/csv/locations_blue.csv',
                './img/colors/csv/locations_snow.csv']
species = ['canada', 'blue', 'snow']

fileCanada = open(csvFilePaths[0], 'wb')
fileBlue = open(csvFilePaths[1], 'wb')
fileSnow = open(csvFilePaths[2], 'wb')
writerCanada = csv.writer(fileCanada)
writerBlue = csv.writer(fileBlue)
writerSnow = csv.writer(fileSnow)

pathToDetector = args["detector"]
detector = dlib.simple_object_detector(pathToDetector)

pathToHistogramIndex = args["histogramIndex"]
pathToROI = args["pathROI"]
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
            species = querySearch.search(roi, pathToHistogramIndex)
            species = species[0:species.find('_')]
            print species

            # rowToWrite = [d.center().x, d.center().y, species]
            # writer.writerow(rowToWrite)
            if species == 'canada':
                writerCanada.writerow([d.center().x, d.center().y])
            elif species == 'blue':
                writerBlue.writerow([d.center().x, d.center().y])
            elif species == 'snow':
                writerSnow.writerow([d.center().x, d.center().y])
            else:
                print "oops"

            roiPath = pathToROI + '/' + species + '_' + imageNames[p] + '_' + str(i) + '.jpg'
            cv2.imwrite(roiPath, roi)

fileCanada.close()
fileBlue.close()
fileSnow.close()

"""
for p in range(len(imagePaths)):
    frame = cv2.imread(imagePaths[p])

    for s in range(len(csvFilePaths)):
        coords = genfromtxt(csvFilePaths[s], delimiter=',')

        n = len(coords)
        d = np.zeros((n, n), dtype=object)
        for i in range(0, n - 1):
            for j in range(1, n):
                if (j != i):
                    # Calculate distance here
                    distance = round(distanceBetweenPointsPixel(coords[i][0], coords[i][1], coords[j][0], coords[j][1]), 2)
                    distanceThreshold = 50 # pixels
                    if (distance < distanceThreshold):
                        cv2.line(frame, (int(coords[i][0]), int(coords[i][1])),
                                 (int(coords[j][0]), int(coords[j][1])), (0, 0, 255), thickness=3)

                    d[i][j] = distance

    timer.log('end')
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""