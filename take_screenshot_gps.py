import cv2
import uuid
import dronekit
import csv

'''
cap is the opencv camera class. cap = cv2.VideoCapture(0)
vehicle is the dronekit vehicle class.
imagePath is where the image will be saved. Leave blank for current directory
csvPath is where the excel file will be saved. Leave blank for default

Then, call take_screenshot every time you want to take a picture

Example:
cap = cv2.VideoCapture(0)
vehicle = connect('......')
take_screenshot(cap, vehicle)


Example:
cap = cv2.VideoCapture(0)
vehicle = connect('......')
imagePath = './img'
csvPath = './test.csv'
take_screenshot(cap, vehicle, imagePath, csvPath)

'''
def take_screenshot(cap, vehicle, imagePath='.', csvPath="./image_gps.csv"):
    ret, img = cap.read()
    file = open(csvPath, 'a')
    writer = csv.writer(file)

    if ret:
        # Save the image to the specified location with a random filename
        filename = imagePath + '/' + str(uuid.uuid4())
        cv2.imwrite(filename, img)

        # Get latitude, longitude, and altitude
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        alt = vehicle.location.global_frame.alt

        # Write row containing the image
        row = [filename, lat, lon, alt]
        writer.writerow(row)

    file.close()