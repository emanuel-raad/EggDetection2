import cv2
import numpy as np
from imageprocessing.contourFinding import filterAreaLow
from imageprocessing.Color import randomColor

img = cv2.imread("./histogram/indexImages/snow_goose_1.jpg")
img = cv2.GaussianBlur(img, (3, 3), 0)

v = np.median(img)
sigma = 0.33
low = int(max(0, (1.0 - sigma) * v))
high = int(min(255, (1.0 + sigma) * v))
edges = cv2.Canny(img, 100, 200)

kernel = np.ones((3, 3), np.uint8)
dilate1 = cv2.dilate(edges, kernel, iterations=1)
erode1 = cv2.erode(dilate1, kernel, iterations=1)

imgContours, contours, h = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Only keep areas above 10,000
MIN_AREA = 1
filteredContours = filterAreaLow(contours, MIN_AREA)

# Draws each contour
for i in filteredContours:
    cv2.drawContours(img, [i], 0, randomColor(), 3)

print "Number of geese: {}".format(len(filteredContours))

cv2.imshow('img', img)
cv2.imshow('edges', erode1)

cv2.waitKey(0)
cv2.destroyAllWindows()