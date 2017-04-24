import cv2
import numpy as np
import math

from sensors.camera import Camera
from utils.timer import Timer

# Blob detection method

lower_white = np.array([0, 0, 150], dtype=np.uint8)
upper_white = np.array([180, 255, 255], dtype=np.uint8)

def initDetectorParams():
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

    return params

def findEgg(img, detector):
    # Filter out white
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower_white, upper_white)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Apply mask
    #filtered = cv2.bitwise_and(img.copy(), img.copy(), mask=mask)
    # Convert to gray for blob detection
    filteredGray = cv2.cvtColor(cv2.bitwise_and(img, img, mask=mask), cv2.COLOR_BGR2GRAY)

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

    # timer = Timer()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    data = np.load('./matrixCalibration.npz')
    cmatrix = data['camera_matrix']
    dist = data['dist_coefs']

    detector = cv2.SimpleBlobDetector_create(initDetectorParams())

    initiateCamera = True

    while True:
        ret, img = cap.read()

        h, w = img.shape[:2]

        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cmatrix, dist, (w, h), 1, (w, h))
        dst = cv2.undistort(img, cmatrix, dist, None, newcameramtx)
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]

        if initiateCamera:
            print "Height: {}\nWidth: {}".format(h, w)
            camera = Camera(w, h, 65.0)
            altitude = 102.0
            print "Full x length: {:.2f} cm".format(2 * camera.getCx(altitude))
            print "Full y length: {:.2f} cm".format(2 * camera.getCy(altitude))
            initiateCamera = False

        # keypoints, f = findEggDebug(img)
        keypoints = findEgg(dst, detector)
        cv2.circle(dst, (w/2, h/2), 5, (255, 0, 0), -1)

        if len(keypoints) > 0:
            # imgk = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            # Loops through every detection, and finds the distance to the center
            distance = []
            for j in range(len(keypoints)):
                x = int(keypoints[j].pt[0])
                y = int(keypoints[j].pt[1])
                distancePixel = math.sqrt(math.pow(w/2.0-x, 2) + math.pow(h/2.0-y, 2))
                distance.append(distancePixel)

            # Finds the shortest distance to the center of the frame
            shortestDistanceIndex = distance.index(min(distance))
            xShort = int(keypoints[shortestDistanceIndex].pt[0])
            yShort = int(keypoints[shortestDistanceIndex].pt[1])

            # Difference between the detection and the center, in pixels
            diffX = xShort - w/2.0
            diffY = -1 * (yShort - h/2.0) # Negative because the pixel coords increase downwards

            # Difference between the detection and the center, in centimeters
            # x: + up (egg is up relative to the center), - down
            # y: + right, - left
            altitude = 103.0
            offsetX = camera.getRealWorldDistance(altitude, diffX)
            offsetY = camera.getRealWorldDistance(altitude, diffY)
            diffR = math.sqrt(offsetX**2 + offsetY**2)

            print "offsetX:{:.2f}\toffsetY:{:.2f}\tdiff:{:.2f} cm".format(offsetX, offsetY, diffR)

            # Draw centroids
            for k in keypoints:
                x = int(k.pt[0])
                y = int(k.pt[1])
                cv2.circle(dst, (x, y), 10, (0, 0, 255), -1)

            if diffR < 1.0:
                cv2.circle(dst, (w/2, h/2), 5, (0, 255, 0), -1)
                cv2.circle(dst, (xShort, yShort), 5, (0, 255, 0), -1)

            # cv2.imshow("filtered", f)
            # cv2.imshow("mask", mask)

        # timer.sinceLastTimeLog('')
        cv2.imshow("img_keypoints", dst)

        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    data.close()

if __name__ == "__main__":
    main()