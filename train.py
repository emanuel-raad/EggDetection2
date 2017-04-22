import argparse
import dlib
import time

"""
1.
Resize images using (WARNING this will overwrite the originals):
mogrify -resize AAAxBBB *.xxx
	AAAxBBB aspect ratio
	xxx filetype
	
mogrify -resize 640x480 *.jpg

2.
Create list of images using:
./imglab -c filename.xml path/to/images

3.
Add borders using:
./imglab filename.xml

If you want to make a bigger sample, but you already have sample1.xml
Then put the new images in a seperate folder, and create sample2.xml
and label the borders.
Then, using notepad, open sample2.xml and copy-paste the information
into sample1.xml.
Then do find+replace to correct the image paths
Finally, retrain using the combined xml file

"""

ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument("-l", "--label", required = True,
	help = "Name of xml file containing all the image labels (made using imglab).\nExample: 'color.xml'")
ap.add_argument("-d", "--detector", required = True,
	help = "Name of detector file that will be created.\nEx: 'detector_color'")
args = vars(ap.parse_args())

start_time = time.time()

options = dlib.simple_object_detector_training_options()
options.C = 50
options.num_threads = 4
options.be_verbose = True
options.epsilon = 0.01

labelsPath = args["label"]
detectorName = args["detector"] + ".svm"

dlib.train_simple_object_detector(labelsPath, detectorName, options)

print("--- %s seconds ---" % (time.time() - start_time))