import cv2

from imageprocessing.eggDetection import findEgg
from utils.timer import Timer


class ROI:
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

def main():
    timer = Timer(debug=True)
    cap = cv2.VideoCapture(0)
    timer.log("start")

    shots = 10
    counter = 0
    width = int(cap.get(3))
    height = int(cap.get(4))

    """
    Position camera in a way to get the egg in the frame,
    then set the ROI to that area of the frame so the rest
    of the image is ignored
    """
    roi = ROI(200, height, 400, width) # Bottom right corner

    """
    Takes n number of screenshots spaced half a second apart, and then
    searches them for an egg uses the blob detection technique. If
    most of the screenshots contain an egg, then the egg has indeed been picked up.
    """
    for i in range(0, shots):
        ret, frame = cap.read()
        timer.sinceLastTimeLog("frame read")
        frameROI = frame[roi.top:roi.bottom, roi.left:roi.right]
        timer.sinceLastTimeLog("roi created")
        keypoints = findEgg(frameROI)
        timer.sinceLastTimeLog("eggs found")
        print len(keypoints)

        if len(keypoints) > 0:
            counter += 1
            for k in keypoints:
                x = int(k.pt[0])
                y = int(k.pt[1])
                cv2.circle(frameROI, (x, y), 20, (0, 0, 255), -1)
        path = "./img/eggROIs/" + str(i) + ".jpg"
        cv2.imwrite(path, frameROI)

        print("Counter: {}").format(counter)
        print("Percentage: {}").format(float(counter)/shots * 100)
        #time.sleep(0.5)

    timer.log("end")
    cap.release()

if __name__=="__main__":
    main()