import dlib
import time

"""

Resize images using (WARNING this will overwrite the originals):
mogrify -resize AAAxBBB *.xxx
	AAAxBBB aspect ratio
	xxx filetype
	
mogrify -resize 640x480 *.jpg

Create list of images using:
./imglab -c filename.xml path/to/images

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

start_time = time.time()

options = dlib.simple_object_detector_training_options()
options.C = 50
options.num_threads = 4
options.be_verbose = True
options.epsilon = 0.01

labelsPath = 'colors.xml'
detectorName = 'detector_colors.svm'

dlib.train_simple_object_detector(labelsPath, detectorName, options)

print("--- %s seconds ---" % (time.time() - start_time))