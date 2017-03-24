import math

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