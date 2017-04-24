import argparse
import cv2
import dlib
import glob
import os
import csv
import numpy as np
import uuid

from utils.timer import Timer
from histogram import querySearch
from imageprocessing.distances import distanceBetweenPointsPixel, addLatitude, addLongitude
from sensors.camera import Camera
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
ap.add_argument("-s", "--pathCSV", required = True,
    help = "Path where the resulting locations will be stored")
args = vars(ap.parse_args())

timer = Timer()

# Filename of images to search
path = args["queryImages"]
imagePaths = glob.glob(path)
imageNames = [os.path.basename(x) for x in imagePaths]
print imageNames

category = ['canada', 'blue', 'snow']

# category = ['red' , 'blue', 'green']

pathCSV = args["pathCSV"]
csvFilePaths = [pathCSV + '/canada.csv',
                pathCSV + '/blue.csv',
                pathCSV + '/snow.csv']


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
            row = [imagePaths[p], d.center().x, d.center().y]
            if species == category[0]:
                writerCanada.writerow(row)
            elif species == category[1]:
                writerBlue.writerow(row)
            elif species == category[2]:
                writerSnow.writerow(row)
            else:
                print "oops"

            filenameUUID = str(uuid.uuid4())
            roiPath = pathToROI + '/' + species + '_' + filenameUUID + '.jpg'
            cv2.imwrite(roiPath, roi)

fileCanada.close()
fileBlue.close()
fileSnow.close()


camera = Camera()
frameCenterX = 640.0/2
frameCenterY = 480.0/2

# Loop through each picture
for p in range(len(imagePaths)):
    frame = cv2.imread(imagePaths[p])
    print imagePaths[p]

    # Loop through each species
    for s in range(len(csvFilePaths)):
        # print csvFilePaths[s]
        coords = genfromtxt(csvFilePaths[s], delimiter=',', dtype=[np.dtype(object), np.dtype(int), np.dtype(int)])
        # print coords
        n = coords.size
        # print n
        d = np.zeros((n, n), dtype=object)

        if n > 0:
            for i in range(0, n - 1):
                for j in range(1, n):
                    # print "Coords for {}".format(coords[i][0])
                    if (j != i) and (coords[i][0] == imagePaths[p]) and (coords[j][0] == imagePaths[p]):
                        # print "Match!"
                        indexPixelX = 1
                        indexPixelY = 2
                        # Calculate distance here
                        distance = round(distanceBetweenPointsPixel(
                            coords[i][indexPixelX], coords[i][indexPixelY], coords[j][indexPixelX], coords[j][indexPixelY]), 2)
                        distanceThreshold = 50 # pixels

                        # 300 cm
                        # distanceThreshold = camera.getRealWorldToPixel(ultrasonic.getAltitude(), 300.0)
                        if (distance < distanceThreshold):
                            cv2.line(frame, (coords[i][indexPixelX], coords[i][indexPixelY]),
                                     (coords[j][indexPixelX], coords[j][indexPixelY]), (0, 0, 255), thickness=3)
                            '''
                            nestCenterX = (coords[i][indexPixelX] - coords[j][indexPixelX]) / 2.0
                            nestCenterY = (coords[i][indexPixelY] - coords[j][indexPixelY]) / 2.0
                            dx = nestCenterX - frameCenterX
                            dy = nestCenterY - frameCenterY
                            newLatitude = addLatitude(latitude, dy)
                            newLongitude = addLongitude(longitude, latitude, dx)
                            '''

                        d[i][j] = distance

    timer.log('end')
    # cv2.imshow('frame', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()