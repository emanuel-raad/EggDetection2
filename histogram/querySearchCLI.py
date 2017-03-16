from searcher import Searcher
from rgbhistogram import RGBHistogram
import numpy as np
import argparse
import cPickle
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images we just indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where we stored our index")
ap.add_argument("-q", "--query", required = True,
	help = "Path to query image")
args = vars(ap.parse_args())

queryImage = cv2.imread(args["query"])
cv2.imshow("Query", queryImage)
print "query: %s" % (args["query"])

desc = RGBHistogram([8, 8, 8])
queryFeatures = desc.describe(queryImage)

index = cPickle.loads(open(args["index"]).read())
searcher = Searcher(index)
results = searcher.search(queryFeatures)

rows = 200
cols = 300
montage = np.zeros((rows * 3, cols, 3), dtype = "uint8")

for j in range(0, 3):
    (score, imageName) = results[j][0]
    path = args["dataset"] + "/%s" % (imageName)
    result = cv2.imread(path)
    result = cv2.resize(result, (cols, rows))
    print "\t%d. %s : %.3f" % (j + 1, imageName, score)

    montage[j * rows:(j + 1) * rows, :] = result

cv2.imshow("Results", montage)
cv2.waitKey(0)