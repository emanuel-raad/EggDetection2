import math

class Camera:
    def __init__(self, rx=640.0, ry=480.0, dfov=78):
        self.dfov = float(dfov)
        self.rx = float(rx)
        self.ry = float(ry)
        self.aspect_ratio = self.ry/self.rx
        self.alpha = math.atan(self.aspect_ratio)
        print "Alpha: {}\nRx: {}\nRy: {}\nAspectRatio: {}".format(self.alpha, self.rx, self.ry, self.aspect_ratio)

    def getCx(self, altitude):
        dx = altitude
        dh = dx / math.cos(math.radians((self.dfov / 2.0)))
        dy = dh * math.sin(math.radians(self.dfov / 2.0))
        return dy * math.cos(self.alpha)

    def getCy(self, altitude):
        dx = altitude
        dh = dx / math.cos(math.radians((self.dfov / 2.0)))
        dy = dh * math.sin(math.radians(self.dfov / 2.0))
        return dy * math.sin(self.alpha)

    def getRealWorldDistance(self, altitude, distancePixel):
        pixelRealRatio = self.getCx(altitude) / (self.rx/2.0)
        distanceReal = distancePixel * pixelRealRatio
        return distanceReal

    def getRealWorldToPixel(self, altitude, distanceReal):
        realPixelRatio = (self.rx/2.0) / self.getCx(altitude)
        distancePixel = distanceReal * realPixelRatio
        return distancePixel