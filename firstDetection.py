import dlib

def firstDetection(frame):

    detector = dlib.simple_object_detector("detector_eggs.svm")
    dets = detector(frame)

    if len(dets) > 0:
        for i, d in enumerate(dets):
            """
            Create a rectangular region of interest around each detection
            Frame is acccessed by pixel [startY:endY, startX:endX]
            """
            roi = frame[d.top():d.bottom(), d.left():d.right()]
            return roi