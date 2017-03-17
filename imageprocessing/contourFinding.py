import cv2
import numpy as np

def contourCanny(roi):
	roi = cv2.GaussianBlur(roi, (5, 5), 0)
	edges = cv2.Canny(roi, 100, 200)
	
	'''
	kernel = np.ones((5, 5), np.uint8)
	roi = cv2.erode(roi, kernel, iterations=2)
	
	kernelDilate = np.ones((5, 5), np.uint8)
	roi = cv2.dilate(roi, kernel, iterations=1)
	'''

	return edges

def filterAreaLow(contours, thresLow):
	filteredAreas = []
	for i in contours:
		if cv2.contourArea(i) >= thresLow:
			filteredAreas.append(i)
	return filteredAreas

def binaryThresholding(roi):
	'''
	hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

	lower = np.array([0, 0, 100])
	upper = np.array([180, 255, 255])

	mask = cv2.inRange(hsv, lower, upper)
	
	res = cv2.bitwise_and(roi,roi, mask=mask)
	cv2.imwrite('bin.jpg', res)
	'''
	
	# Reads the image and does color filtration
	img = roi
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	a = [0, 0, 100]
	b = [180, 255, 255]

	lower_white = np.array([30,0,230])
	upper_white = np.array([180,255,255])

	mask = cv2.inRange(hsv, lower_white, upper_white)
	print 'writing mask'
	cv2.imwrite('mask.jpg', mask)
	"""
	res = cv2.bitwise_and(img,img, mask= mask)

	#cv2.imwrite('eggafterfiltration.jpg', res)

	# Reads the image after colour filtration and converts to gray, does threshold, opening, closing


	ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

	kernel = np.ones((2,2),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
	closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, np.ones((2,2),np.uint8),iterations=2)

	#cv2.imshow('thres', closing)

	# This will give us the binary image of the egg. Then we can use contours and similarity.
	#cv2.imwrite('Binaryegg1.jpg', closing)
	"""
	return closing



