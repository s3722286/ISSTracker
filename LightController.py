#!/usr/bin/env python3
from sense_hat import SenseHat
import time

class LightController:
    s = SenseHat()
    s.set_rotation(270)

    red = (255, 0, 0)
    orange = (255, 128, 0)
    yellow = (200, 200, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    off = (0, 0, 0)
    allOff = [off for i in range(64)]

    redTuple = (red, range(0,8), (0, 7))
    orangeTuple = (orange, range(1,7), (1, 6))
    yellowTuple = (yellow, range(2,6), (2, 5))
    greenTuple = (green, range(3,5), (3, 4))
    blueTuple = (blue, range(3,5), (3, 4))


    def drawDirection(angle, direction):

        incline = 0

        if(angle < 0):
            incline = 1
            angle = abs(angle)

        if(angle > 30):
            drawLine(redTuple, incline, direction)
        elif(angle > 10):
            drawLine(orangeTuple, incline, direction)
        elif(angle > 3):
            drawLine(yellowTuple, incline, direction)
        elif(angle > 1):
            drawLine(greenTuple, incline, direction)
        else:
            drawLine(blueTuple, incline, direction)

    def drawLine(colorTuple, isNegative, direction):
        if(direction == "vertical"):
            X = colorTuple[1]
            Y = colorTuple[2][isNegative]

            for x in X:
                s.set_pixel(x, Y, colorTuple[0])
        else:
            X = colorTuple[2][isNegative]
            Y = colorTuple[1] 

            for y in Y:
                s.set_pixel(X, y, colorTuple[0]) 

   
if __name__ == '__main__':
     
    anglRange = range(35, -36, -1)

    for angl in anglRange:
        angl2 = abs(angl)
        print(str(angl) + " " + str(angl2))
        
        drawDirection(angl, "vertical")
        drawDirection(angl2, "horizontal")
        time.sleep(0.1)
        s.set_pixels(allOff)


