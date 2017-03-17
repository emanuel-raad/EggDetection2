import cv2

def removeColor(image, colorLow, colorHigh):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLow, colorHigh)
    maskInv = cv2.bitwise_not(mask)

    filtered = cv2.bitwise_and(image, image, mask=maskInv)
    return filtered

def keepColor(image, colorLow, colorHigh):
    mask = cv2.inRange(image, colorLow, colorHigh)

    filtered = cv2.bitwise_and(image, image, mask=mask)
    return filtered

def combineMask(masks):
    combinedMask = masks[0]
    for i in (range(0, len(masks)-1)):
        print i
        combinedMask = cv2.bitwise_or(combinedMask, masks[i+1])

    return combinedMask