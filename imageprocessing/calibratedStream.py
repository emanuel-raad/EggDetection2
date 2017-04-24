import cv2
import numpy as np

from sensors.camera import Camera

with np.load('./matrixCalibration.npz') as data:
    cmatrix = data['camera_matrix']
    dist = data['dist_coefs']
    rvecs = data['rotation']
    tvecs = data['trans']

    print cmatrix

    cap = cv2.VideoCapture(0)
    once = True

    while True:
        ret, img = cap.read()

        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cmatrix, dist, (w, h), 1, (w, h))

        # undistort
        dst = cv2.undistort(img, cmatrix, dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        if once:
            print "Height: {}\nWidth: {}".format(h, w)
            camera = Camera(w, h, 65.0)
            altitude = 102.0
            print "Full x length: {:.2f} cm".format(2 * camera.getCx(altitude))
            print "Full y length: {:.2f} cm".format(2 * camera.getCy(altitude))
            once = False

        cv2.imshow('distorted', img)
        cv2.imshow('undistorted', dst)
        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()