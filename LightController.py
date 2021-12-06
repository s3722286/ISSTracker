#!/usr/bin/env python3
from sense_hat import SenseHat
import time

class LightController:

    def __init__(self):
        self.s = SenseHat()
        self.s.set_rotation(270)

        red = (255, 0, 0)
        orange = (255, 128, 0)
        yellow = (200, 200, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        self.allOff = [(0, 0, 0) for i in range(64)]

        self.redTuple = (red, range(0,8), (0, 7))
        self.orangeTuple = (orange, range(1,7), (1, 6))
        self.yellowTuple = (yellow, range(2,6), (2, 5))
        self.greenTuple = (green, range(3,5), (3, 4))
        self.blueTuple = (blue, range(3,5), (3, 4))

    def drawLine(self, colorTuple, isNegative, direction):
        if(direction == "vertical"):
            X = colorTuple[1]
            Y = colorTuple[2][isNegative]

            for x in X:
                self.s.set_pixel(x, Y, colorTuple[0])
        else:
            X = colorTuple[2][isNegative]
            Y = colorTuple[1] 

            for y in Y:
                self.s.set_pixel(X, y, colorTuple[0]) 

    def drawDirection(self, angle, direction):

        incline = 0

        if(angle < 0):
            incline = 1
            angle = abs(angle)

        if(angle > 30):
            self.drawLine(self.redTuple, incline, direction)
        elif(angle > 10):
            self.drawLine(self.orangeTuple, incline, direction)
        elif(angle > 3):
            self.drawLine(self.yellowTuple, incline, direction)
        elif(angle > 1):
            self.drawLine(self.greenTuple, incline, direction)
        else:
            self.drawLine(self.blueTuple, incline, direction)

    def clearDisplay(self):
        self.s.set_pixels(self.allOff)




if __name__ == '__main__':
     
    LC = LightController()
    anglRange = range(35, -36, -1)

    for angl in anglRange:
        angl2 = abs(angl)
        print(str(angl) + " " + str(angl2))
        
        LC.drawDirection(angl, "vertical")
        LC.drawDirection(angl2, "horizontal")
        time.sleep(0.1)
        LC.clearDisplay()
        


