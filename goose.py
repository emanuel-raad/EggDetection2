import cv2
import numpy as np
import random

#Uncomment in case you need to use trackbars to find the canny thresholds
def nothing(x):
    pass

cv2.namedWindow('canny')
cv2.createTrackbar('low', 'canny', 0, 1000, nothing)
cv2.createTrackbar('high', 'canny', 0, 1000, nothing)

# Random color for drawing
def randomColor():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r, g, b)

#Filters a contour array by low bound
def filterAreaLow(contours, thresLow):
    filteredAreas = []
    for i in contours:
        if cv2.contourArea(i) >= thresLow:
            filteredAreas.append(i)
    return filteredAreas


frame = cv2.imread('./histogram/indexImages/blue_1.jpg', 1)
cv2.namedWindow('frame')

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_blue = np.array([0, 0, 0])
upper_blue = np.array([179, 42, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(frame, frame, mask=mask)

res = cv2.GaussianBlur(res, (5, 5), 0)

kernel = np.ones((7, 7), np.uint8)
erosion = cv2.erode(res, kernel, iterations=2)
im = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)

#Uncomment in case you need to use trackbars to find the canny thresholds
while True:
    l = cv2.getTrackbarPos('low', 'canny')
    h = cv2.getTrackbarPos('high', 'canny')
    edges = cv2.Canny(im, l, h)
    cv2.imshow('canny', edges)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

# Use canny edge to find outline after erosion
# edges = cv2.Canny(im, 206, 438)

# Dilate the lines to join them and form one contour
kernelDilate = np.ones((5, 5), np.uint8)
edges = cv2.dilate(edges, kernel, iterations=1)

cv2.imshow('edges', edges)

# Finds the contours. Use cv2.RETR_EXTERNAL to only get the outer contour for the thick edge
imgContours, contours, h = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Only keep areas above 10,000
MIN_AREA = 10000
filteredContours = filterAreaLow(contours, MIN_AREA)

# Draws each contour
for i in filteredContours:
    cv2.drawContours(frame, [i], 0, randomColor(), 3)

print "Number of geese: {}".format(len(filteredContours))
cv2.imshow('frame', frame)
cv2.imwrite("contour.jpg", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()