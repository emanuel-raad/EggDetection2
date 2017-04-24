import argparse
import cv2
import dlib
import glob
import os
import uuid

from utils.timer import Timer

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required = True,
	help = "Path to where the detector is stored")
ap.add_argument("-q", "--queryImages", required = True,
	help = "Path to image to search through")
ap.add_argument("-r", "--pathROI", required = True,
	help = "Path to store the detections")
args = vars(ap.parse_args())

timer = Timer()

# Filename of images to search
path = args["queryImages"]
print path
imagePaths = glob.glob(path)
print imagePaths
imageNames = [os.path.basename(x) for x in imagePaths]
print imageNames

pathToROI = args["pathROI"]
pathToDetector = args["detector"]
detector = dlib.simple_object_detector(pathToDetector)


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
            filename = str(uuid.uuid4())
            roiPath = pathToROI + '/'  + filename + '.jpg'
            cv2.imwrite(roiPath, roi)
