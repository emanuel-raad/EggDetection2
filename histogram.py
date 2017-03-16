import cv2
from firstDetection import firstDetection
import numpy as np
from matplotlib import pyplot as plt

#http://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/

def calculateGrayHistogram(img, mask=None):
    hist = cv2.calcHist([img], [0], mask, [256], [0, 256])
    return hist

def main():
    baseImg = cv2.imread('img/egg1.jpg', 0)
    compareImg = cv2.imread('img/egg2.jpg', 0)
    baseHist = calculateGrayHistogram(baseImg)
    compareHist = calculateGrayHistogram(compareImg)

    roiEgg = firstDetection(baseImg)
    roiEgg2 = firstDetection(compareImg)
    roiEggHist = calculateGrayHistogram(roiEgg)
    roiEgg2Hist = calculateGrayHistogram(roiEgg2)

    ret, otsu = cv2.threshold(roiEgg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret, otsu2 = cv2.threshold(roiEgg2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    otsuHist = calculateGrayHistogram(roiEgg, otsu)
    otsuHist2 = calculateGrayHistogram(roiEgg2, otsu2)

    correlationBase = cv2.compareHist(baseHist, compareHist, cv2.HISTCMP_CORREL)
    correlationRoi = cv2.compareHist(roiEggHist, roiEgg2Hist, cv2.HISTCMP_CORREL)
    correlationOtsu = cv2.compareHist(otsuHist, otsuHist2, cv2.HISTCMP_CORREL)

    print("Base correlation: {}").format(correlationBase)
    print("Base correlation: {}").format(correlationRoi)
    print("Base correlation: {}").format(correlationOtsu)

    plt.figure(1)
    plt.subplot(221); plt.imshow(otsu, cmap='Greys')
    plt.subplot(222); plt.imshow(roiEgg, cmap='Greys')
    plt.subplot(223); plt.imshow(otsu2, cmap='Greys')
    plt.subplot(224); plt.imshow(roiEgg2, cmap='Greys')
    plt.show()

    plt.figure(2)
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(baseHist)
    plt.plot(compareHist)
    plt.plot(roiEggHist)
    plt.plot(roiEgg2Hist)
    plt.plot(otsuHist)
    plt.plot(otsuHist2)
    plt.xlim([0, 256])
    plt.show()

    '''
    #plt.hist(baseImg.ravel(), 256, [0, 256])
    #plt.hist(compareImg.ravel(), 256, [0, 256])

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

if __name__ == "__main__":
    main()