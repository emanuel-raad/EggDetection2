import cv2
import numpy as np
import time

# Blob detection method

lower_white = np.array([0, 0, 150], dtype=np.uint8)
upper_white = np.array([180, 255, 255], dtype=np.uint8)

def findEgg(img):
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

    params.filterByCircularity = False

    params.filterByConvexity = True
    params.minConvexity = 0.9
    """
    params.filterByCircularity = True
    params.minCircularity = 0.8
    """

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(filteredGray)

    return keypoints, filteredGray

def main():
    #img = cv2.imread("../img/egg3.jpg")

    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()

        keypoints, f = findEggDebug(img)

        start_time = time.time()
        imgk = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # print("--- %s seconds ---" % (time.time() - start_time))

        # Draw centroids
        for k in keypoints:
            x = int(k.pt[0])
            y = int(k.pt[1])
            cv2.circle(imgk, (x, y), 10, (0, 0, 255), -1)

        cv2.imshow("filtered", f)
        # cv2.imshow("mask", mask)
        cv2.imshow("img_keypoints", imgk)

        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()