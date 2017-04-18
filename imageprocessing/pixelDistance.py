import math

#Logitech C920 Pro. 16:9 aspect ratio. Degrees
C920_DFOV_169 = 78.0

def distanceBetweenPointsPixel(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

def distanceBetweenPointsGPS(lat1, lon1, lat2, lon2):
    R = 6371e3 #Earth's radius
    lat1Rad = math.radians(lat1)
    lat2Rad = math.radians(lat2)
    deltaLat = math.radians(lat2 - lat1)
    deltaLon = math.radians(lon2 - lon1)

    a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) \
        + math.cos(lat1Rad) * math.cos(lat2Rad) \
        * math.sin(deltaLon / 2) * math.sin(deltaLon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c

    return d

def distanceToRealWorld(altitude, distancePixel, halfWidth, camera = 'C910'):
    if camera == 'C920':
        dfov = C920_DFOV_169
        aspect_ratio = 9.0/16.0
    elif camera == 'C910':
        dfov = 83.0
        aspect_ratio = 3.0/4.0
    else:
        dfov = 80
        aspect_ratio = 9/16

    dx = altitude
    dh = dx / math.cos(math.radians((dfov/2)))
    dy = dh * math.sin(math.radians(dfov/2))
    alpha = math.atan(aspect_ratio)
    cx = dy * math.cos(alpha)
    cy = dy * math.sin(alpha)
    print "cx: {}".format(cx)
    print "cy: {}".format(cy)
    pixelRealRatio = cx/halfWidth
    distanceReal = distancePixel * pixelRealRatio

    return distanceReal