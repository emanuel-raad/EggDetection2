import cv2
import numpy as np
#import xlsxwriter
#
## making the new excel worksheet
#workbook = xlsxwriter.Workbook('Data.xlsx')
#worksheet = workbook.add_worksheet('Sheet 1')
#
##adding the bold format to use to highlight the cells
#bold = workbook.add_format({'bold': True})


def nothing(x):
    pass

cap = cv2.imread('test.jpg',1)
cv2.namedWindow('image')

cv2.createTrackbar('hueL','image',0,179,nothing)
cv2.createTrackbar('hueH','image',0,179,nothing)

cv2.createTrackbar('satL','image',0,255,nothing)
cv2.createTrackbar('satH','image',0,255,nothing)

cv2.createTrackbar('ValL','image',0,100,nothing)
cv2.createTrackbar('ValH','image',0,255,nothing)

hl=110
hh=130

sl=50
sh=255

vl=50
vh=255

while(1):

    # Take each frame
    
    # input file name
    frame = cv2.imread('geese.png',1)
    
    

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([hl,sl,0])
    upper_blue = np.array([hh,sh,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

#    cv2.imshow('frame',frame)
#    cv2.imshow('mask',mask)
#    cv2.imshow('res',res)
#     res = cv2.GaussianBlur(res, (5,5),0)
    cv2.imshow('image',res)
    
    hl = cv2.getTrackbarPos('hueL','image')
    hh = cv2.getTrackbarPos('hueH','image')
    
    sl = cv2.getTrackbarPos('satL','image')
    sh = cv2.getTrackbarPos('satH','image')
    
    vl = cv2.getTrackbarPos('valL','image')
    vh = cv2.getTrackbarPos('valH','image')
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        
#        # Widen the column to make the text clearer.
#        worksheet.set_column('A:A', 20)
#        worksheet.set_column('B:B', 10)
#    
#        # Printing the text in column A
#        worksheet.write('A1', 'Values to use in filtering', bold)
#        worksheet.write('B1', 'Values', bold)
#        worksheet.write('A2', 'hl')
#        worksheet.write('A3', 'hh')
#        worksheet.write('A4', 'sl')
#        worksheet.write('A5', 'sh')
#        worksheet.write('A6', 'v1')
#        worksheet.write('A7', 'vh')
#        
#        
#        #Printing the actual values in column B
#        worksheet.write('B2', hl)
#        worksheet.write('B3', hh)
#        worksheet.write('B4', sl)
#        worksheet.write('B5', sh)
#        worksheet.write('B6', vl)
#        worksheet.write('B7', vh)

    	
    	# values to use in filtering
    	cv2.imwrite('test.png',res)
    	print hl
    	print hh
    	print sl
    	print sh
    	print vl
    	print vh
        break

#workbook.close()
cv2.destroyAllWindows()
