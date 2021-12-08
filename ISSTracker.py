#!/usr/bin/env python3
from sense_hat import SenseHat
import time
import math
import requests
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

        self.targetAltitudeAngle = 0
        self.targetAzimuthAngle = 0

    def calcDirectionToISS(self):
        url = "https://api.wheretheiss.at/v1/satellites/25544"
        response = requests.get(url)

        if(response.status_code == 200):

            ISSData = response.json()
            self.calcDirectionToTarget(ISSData['latitude'], ISSData['longitude'], ISSData['altitude'] * 1000)

        else:
            print("API call failed. Status Code: " + str(response.status_code))

    def calcDirectionToTarget(self, latitude, longitude, altitude):

        selfLatRad = math.radians(self.Lat)
        selfLonRad = math.radians(self.Lon)
        targetLatRad = math.radians(latitude)
        targetLonRad = math.radians(longitude)

        latDiff = selfLatRad - targetLatRad
        lonDiff = selfLonRad - targetLonRad

        # Calculating Azimuth Angle
        varX = math.cos(targetLatRad) * math.sin(lonDiff)
        varY = math.cos(selfLatRad) * math.sin(targetLatRad) - math.sin(selfLatRad) * math.cos(targetLatRad) * math.cos(lonDiff)
        

        bearing = math.atan2(varX, varY)
        self.targetAzimuthAngle = math.degrees(bearing) * -1
        print("degBearing: " + str(self.targetAzimuthAngle))


        # Calculating Altitude Angle
        earthRadius = 6371 # in kilometres
        p = (math.pi / 180)

        aVar = math.sin(latDiff / 2)**2 + math.cos(selfLatRad) * math.cos(targetLatRad) * math.sin(lonDiff / 2)**2
        cVar = 2 * math.atan2(math.sqrt(aVar), math.sqrt(1 - aVar))
        GCDistance = earthRadius * cVar
        print("Great Circle Distance: " + str(GCDistance))

        innerAngleRad = GCDistance / earthRadius
        selfDistanceFromCenter = 6371 * 1000 + self.Alt
        targetDistanceFromCenter = 6371 * 1000 + altitude

        directDistance = math.sqrt(selfDistanceFromCenter**2 + targetDistanceFromCenter**2 - 2 * selfDistanceFromCenter * targetDistanceFromCenter * math.cos(innerAngleRad))
        acosInput = (selfDistanceFromCenter**2 + directDistance**2 - targetDistanceFromCenter**2) / (2 * targetDistanceFromCenter * directDistance)
        
        if(acosInput < -1):
            acosInput = -1
        elif(acosInput > 1):
            acosInput = 1
        
        self.targetAltitudeAngle = math.degrees(math.acos(acosInput)) - 90
        print("altitudeAngle: " + str(self.targetAltitudeAngle))




    def directionToTarget(self):

        Orientation = self.Sens.getOrientation()
        #print(Orientation["yaw"])
        
        verticalAngle = self.targetAltitudeAngle - Orientation["pitch"]
        
        if(verticalAngle < -180): 
            verticalAngle = verticalAngle + 360
        if(verticalAngle > 180): 
            verticalAngle = verticalAngle - 360

        horizontalAngle = self.targetAzimuthAngle - Orientation["yaw"]

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
    #IssTracker.calcDirectionToTarget(-37.82157683248408, 144.9646339973411, 297.3)
    i = 0
    while(True):
        i = i + 1
        if(i % 40 == 0):
            IssTracker.calcDirectionToISS()
        IssTracker.directionToTarget()
        time.sleep(0.05)

    IssTracker.LC.clearDisplay()

except:

    IssTracker.LC.clearDisplay()
    


    