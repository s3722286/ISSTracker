#!/usr/bin/env python3
from sense_hat import SenseHat
import time
import math
from LightController import LightController
from Sensors import Sensors

class ISSTracker:

    def __init__(self):
        self.s = SenseHat()
        self.Sens = Sensors(self.s)
        self.LC = LightController(self.s)

        #These are taken from location.txt
        f = open("location.txt", "r")
        location = f.readline().split(",")
        #print(location)
        f.close()
        
        self.Lat = float(location[0])
        self.Lon = float(location[1])
        self.Alt = float(location[2])

        self.targetAltitude = 0
        self.targetAzimuth = 0

    def calcDirectionToTarget(self, latitude, longitude, altitude):
        #print(latitude)

        longDifference = longitude - self.Lon
        print("longDifference: " + str(longDifference))
        varX = math.cos(math.radians(latitude)) * math.sin(math.radians(longDifference))
        varY = math.cos(math.radians(self.Lat)) * math.sin(math.radians(latitude)) - math.sin(math.radians(self.Lat)) * math.cos(math.radians(latitude)) * math.cos(math.radians(longDifference))
        print("1: " + str(math.cos(math.radians(self.Lat))))
        print("2: " + str(math.sin(math.radians(latitude))))
        print("3: " + str(math.sin(math.radians(self.Lat))))
        print("4: " + str(math.cos(math.radians(latitude))))
        print("5: " + str(math.cos(math.radians(longDifference))))
        print("varX: " + str(varX))        
        print("varY: " + str(varY))
        
        bearing = math.atan2(varX, varY)
        print("radbearing: " + str(bearing))

        self.targetAzimuth = math.degrees(bearing)
        print("degBearing: " + str(self.targetAzimuth))

        self.targetAltitude = 0



    def directionToTarget(self):

        Orientation = self.Sens.getOrientation()
        #print(Orientation["yaw"])
        
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
    IssTracker.calcDirectionToTarget(90, 0, 0) #mag north(86.4,-156.768, 0)

    while(True):
        IssTracker.directionToTarget()
        time.sleep(0.05)
    IssTracker.LC.clearDisplay()

except:

    IssTracker.LC.clearDisplay()
    


    