from searcher import Searcher
from rgbhistogram import RGBHistogram
import numpy as np
import cPickle
import cv2

indexPath = "./histogramIndex"
datasetPath = "./indexImages"

def search(queryImage, mask=None):
    cv2.imshow("Query", queryImage)

    desc = RGBHistogram([8, 8, 8])
    queryFeatures = desc.describe(queryImage)

    index = cPickle.loads(open(indexPath).read())
    searcher = Searcher(index)
    results = searcher.search(queryFeatures)

    rows = 200
    cols = 300
    montage = np.zeros((rows * 3, cols, 3), dtype = "uint8")

    for j in range(0, 3):
        (score, imageName) = results[j][0]
        path = datasetPath + "/%s" % (imageName)
        result = cv2.imread(path)
        result = cv2.resize(result, (cols, rows))
        print "\t%d. %s : %.3f" % (j + 1, imageName, score)

        montage[j * rows:(j + 1) * rows, :] = result

    cv2.imshow("Results", montage)
    cv2.waitKey(0)

def main():
    img = cv2.imread("queryImages/canada_goose_1.jpg")
    search(img)

if __name__ == "__main__":
    main()