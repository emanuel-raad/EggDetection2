import cv2
import numpy as np

from imageprocessing.pixelDistance import distanceBetweenPointsPixel, distanceToRealWorld
from utils.timer import Timer

# Blob detection method

lower_white = np.array([0, 0, 150], dtype=np.uint8)
upper_white = np.array([180, 255, 255], dtype=np.uint8)

center_y = 480/2
center_x = 640/2

def findEgg(img):
    # Filter out white
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower_white, upper_white)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Apply mask
    #filtered = cv2.bitwise_and(img.copy(), img.copy(), mask=mask)
    # Convert to gray for blob detection
    filteredGray = cv2.cvtColor(cv2.bitwise_and(img, img, mask=mask), cv2.COLOR_BGR2GRAY)

    # Blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 200

    params.filterByColor = True
    params.blobColor = 255

    params.filterByCircularity = False

    params.filterByConvexity = True
    params.minConvexity = 0.9
    """
    params.filterByCircularity = True
    params.minCircularity = 0.8
    """

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(filteredGray)

    return keypoints

def findEggDebug(img):
    # Filter out white
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower_white, upper_white)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Apply mask
    #filtered = cv2.bitwise_and(img.copy(), img.copy(), mask=mask)
    # Convert to gray for blob detection
    filteredGray = cv2.cvtColor(cv2.bitwise_and(img, img, mask=mask), cv2.COLOR_BGR2GRAY)

    # Blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 200

    params.filterByColor = True
    params.blobColor = 255

    params.filterByConvexity = True
    params.minConvexity = 0.9

    params.filterByCircularity = True
    params.minCircularity = 0.8

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(filteredGray)

    return keypoints, filteredGray

def main():
    #img = cv2.imread("../img/egg3.jpg")

    timer = Timer()
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        keypoints, f = findEggDebug(img)

        if len(keypoints) > 0:
            print 'ok'
            # imgk = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            # Loops through every detection, and finds the distance to the center
            distance = []
            for j in range(len(keypoints)):
                x = int(keypoints[j].pt[0])
                y = int(keypoints[j].pt[1])
                distance.append(abs(distanceBetweenPointsPixel(center_x, center_y, x, y)))

            # Finds the shortest distance to the center of the frame
            shortestDistanceIndex = distance.index(min(distance))
            x = int(keypoints[shortestDistanceIndex].pt[0])
            y = int(keypoints[shortestDistanceIndex].pt[1])

            # Difference between the detection and the center, in pixels
            diffX = x - center_x
            diffY = y - center_y

            # Difference between the detection and the center, in centimeters
            # x: + up (egg is up relative to the center), - down
            # y: + right, - left
            altitude = 100
            offsetX = distanceToRealWorld(altitude, diffX, center_x)
            offsetY = distanceToRealWorld(altitude, diffY, center_y)

            print "offsetX: {}     offsetY: {}".format(offsetX, offsetY)

            # Draw centroids
            for k in keypoints:
                x = int(k.pt[0])
                y = int(k.pt[1])
                cv2.circle(img, (x, y), 10, (0, 0, 255), -1)

            timer.sinceLastTimeLog('')
            # cv2.imshow("filtered", f)
            # cv2.imshow("mask", mask)
            cv2.imshow("img_keypoints", img)

            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()