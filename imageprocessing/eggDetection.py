import cv2
import numpy as np

# Blob detection method

def main():
    #img = cv2.imread("../img/egg3.jpg")

    cap = cv2.VideoCapture(1)

    while True:
        ret, img = cap.read()

        # Filter out white
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 180], dtype=np.uint8)
        upper_white = np.array([180, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(imgHSV, lower_white, upper_white)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Apply mask
        filtered = cv2.bitwise_and(img.copy(), img.copy(), mask=mask)
        # Convert to gray for blob detection
        filteredGray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

        # Blob detection
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 200

        params.filterByColor = True
        params.blobColor = 255

        """
        params.filterByConvexity = True
        params.minConvexity = 0.9

        params.filterByCircularity = True
        params.minCircularity = 0.8
        """

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(filteredGray)
        imgk = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Draw centroids
        for k in keypoints:
            x = int(k.pt[0])
            y = int(k.pt[1])
            cv2.circle(imgk, (x, y), 1, (0, 0, 255), -1)

        cv2.imshow("filtered", filteredGray)
        cv2.imshow("mask", mask)
        cv2.imshow("img_keypoints", imgk)
        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()