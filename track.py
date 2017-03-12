import cv2
import dlib
import numpy as np
import time
from Color import randomColor
from contourFinding import contourCanny
from contourFinding import binaryThresholding

start_time = time.time()

detector = dlib.simple_object_detector("detector_eggs.svm")
cv2.namedWindow('window')
green = (0, 255, 0)

frame = cv2.imread('img/egg3.jpg')
rows,cols = frame.shape[:2]

dets = detector(frame)

if len(dets) > 0:
	for i, d in enumerate(dets):
		color = randomColor()
		
		"""
		Create a rectangular region of interest around each detection
		Frame is acccessed by pixel [startY:endY, startX:endX]
		"""
		roi = frame[d.top():d.bottom(), d.left():d.right()]
		cv2.imshow('roi', roi)
		
		# Find contours using canny method. See contoursFinding.py
		edges = contourCanny(roi)
		#binary = binaryThresholding(roi)
		
		# Find contours based on edges, and keep the largest one by area
		im, cnts, h= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		#cnts, h = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		if len(cnts) < 1:
			print "no contours"
			break
		
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
		cnts = cnts[0]
		
		#cv2.imshow('edges', edges)
		
		"""
		The pixel coordinates of cnts correspond to pixels on the ROI
		They need to be shifted to fit on the original image to draw
		it properly. 
		[:,0] access first column. x values
		[:,1] access second column. y values
		"""
		cnts[:,0][:,0] = cnts[:,0][:,0] + d.left()
		cnts[:,0][:,1] = cnts[:,0][:,1] + d.top()
		
		"""
		Approximates a shape for the contours. Helpful if the contours
		is not closed.
		"""
		
		#epsilon = 0.01*cv2.arcLength(cnts,True)
		#approxCnt = cv2.approxPolyDP(cnts,epsilon,True)
		approxCnt = cv2.convexHull(cnts)
		
		"""
		Find largest line in contour
		"""
		[vx,vy,x,y] = cv2.fitLine(approxCnt, cv2.DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y)
		righty = int(((cols-x)*vy/vx)+y)
		cv2.line(frame,(cols-1,righty),(0,lefty),color,2)

		cv2.drawContours(frame, [approxCnt], 0, (0, 255, 0), 3)
		#cv2.drawContours(frame, [cnts], 0, (0, 255, 0), 3)

		#cv2.imshow('canny', edges)
		#path = 'roi_' + str(i) + '.jpg'
		#cv2.imwrite(path, roi)
		cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), color, 2)

print("--- %s seconds ---" % (time.time() - start_time))

cv2.imshow('window', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
