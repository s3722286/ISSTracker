#!/usr/bin/env python3
from sense_hat import SenseHat
import time
from LightController import LightController
from Sensors import Sensors

class ISSTracker:

    def __init__(self):
        self.s = SenseHat()
        self.Sens = Sensors(self.s)
        self.LC = LightController(self.s)

        #These will be taken from location.txt
        self.Lat = 0
        self.Lon = 0
        self.Alt = 0

        self.targetAltitude = 0
        self.targetAzimuth = 0

    def calcDirectionToTarget(self, latitude, longitude, altitude):
        self.targetAltitude = 0
        self.targetAzimuth = 0


    def directionToTarget(self):

        Orientation = self.Sens.getOrientation()
        
        verticalAngle = self.targetAltitude - Orientation["pitch"]
        
        if(verticalAngle < -180): 
            verticalAngle = verticalAngle + 360
        if(verticalAngle > 180): 
            verticalAngle = verticalAngle - 360

        horizontalAngle = self.targetAzimuth - Orientation["yaw"]

        if(horizontalAngle < -180): 
            horizontalAngle = horizontalAngle + 360
        if(horizontalAngle > 180): 
            horizontalAngle = horizontalAngle - 360

        self.displayDirectionToTarget(verticalAngle,horizontalAngle)


    def displayDirectionToTarget(self, verticalAng, horizontalAng):

        self.LC.drawDirection(verticalAng, "vertical")
        self.LC.drawDirection(horizontalAng, "horizontal")




if __name__ == '__main__':
    IssTracker = ISSTracker()

try:
    IssTracker.calcDirectionToTarget(0, 0, 0)

    while(True):
        IssTracker.directionToTarget()
        time.sleep(0.05)
        #IssTracker.LC.clearDisplay()

except:

    IssTracker.LC.clearDisplay()


    