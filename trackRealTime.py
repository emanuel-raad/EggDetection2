import cv2
import dlib
import numpy as np
from Color import randomColor
import time
from contourFinding import contourCanny
from contourFinding import binaryThresholding

detector = dlib.simple_object_detector("detector_eggs.svm")
cv2.namedWindow('window')
cap = cv2.VideoCapture(1)

_, frame = cap.read()
rows,cols = frame.shape[:2]

"""
use canny to find contour of roi
then keep only the largest contour, since there's only supposed
to be one egg per roi
then use rajs method to draw the line
"""

while True:
	start_time = time.time()
	print rows
	print cols
	
	print("--- %s seconds READ START---" % (time.time() - start_time))
	_, frame = cap.read()
	print("--- %s seconds READ END. DETECT START---" % (time.time() - start_time))
	dets = detector(frame)
	print("--- %s seconds DETECT---" % (time.time() - start_time))
	
	print "Detections: {}".format(len(dets))
	
	if len(dets) > 0:
		for i, d in enumerate(dets):
			#color = randomColor()
			color = (0, 255, 0)
			"""
			Create a rectangular region of interest around each detection
			Frame is acccessed by pixel [startY:endY, startX:endX]
			"""
			
			roi = frame[d.top():d.bottom(), d.left():d.right()]
			cv2.imshow('roi', roi)
			
			# Find contours using canny method. See contoursFinding.py
			edges = contourCanny(roi)
			#binary = binaryThresholding(roi)
			
			#cv2.imshow('canny', edges)
			
			# Find contours based on edges, and keep the largest one by area
			im, cnts, h = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			#cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			if len(cnts) < 1:
				print "no contours"
				break

			cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
			cnts = cnts[0]
			
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
			
			epsilon = 0.01*cv2.arcLength(cnts,True)
			#approxCnt = cv2.approxPolyDP(cnts,epsilon,True)
			approxCnt = cv2.convexHull(cnts)
			
			"""
			Find largest line in contour. Dont really know how it works,
			gotta ask Raj
			"""
			[vx,vy,x,y] = cv2.fitLine(approxCnt, cv2.DIST_L2,0,0.01,0.01)
			lefty = int((-x*vy/vx) + y)
			righty = int(((cols-x)*vy/vx)+y)
			
			cv2.line(frame,(cols-1,righty),(0,lefty),color,2)

			cv2.drawContours(frame, [approxCnt], 0, color, 3)
			#cv2.drawContours(frame, [cnts], 0, (0, 255, 0), 3)
			path = 'roi_' + str(i) + '.jpg'
			cv2.imwrite(path, roi)
			#cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), color, 2)

	
	print("--- %s seconds ALL ---" % (time.time() - start_time))
	
	cv2.imshow('window', frame)
	k = cv2.waitKey(25) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
