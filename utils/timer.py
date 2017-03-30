import time

class Timer:
    def __init__(self, debug=True):
        self.start = time.time()
        self.debug = debug
        self.lastTime = 0

    def setDebug(self, debug):
        self.debug = debug

    def setLastTime(self):
        self.lastTime = time.time()

    def log(self, message):
        self.lastTime = time.time()
        delTime = time.time() - self.start
        if self.debug:
            message = str.upper(message)
            print "--- {} seconds {}".format(delTime, message)

    def sinceLastTime(self):
        return time.time() - self.lastTime

    def sinceLastTimeLog(self, message):
        delTime = time.time() - self.lastTime
        if self.debug:
            message = str.upper(message)
            print "--- {} seconds STEP: {}".format(delTime, message)
        self.lastTime = time.time()