from HSVTrackbar import HSVTrackbar
import cv2
import numpy as np
import Queue

HSV_WINDOW = 'hsv'
cv2.namedWindow(HSV_WINDOW)

queue = Queue.Queue(maxsize=5)

imgPath = './histogram/indexImages/blue_goose_1.jpg'
original = cv2.imread(imgPath)
s = HSVTrackbar(queue, HSV_WINDOW, original)

print 'main continue'

cv2.waitKey(0)
cv2.destroyAllWindows()
