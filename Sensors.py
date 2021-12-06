#!/usr/bin/env python3
from sense_hat import SenseHat
import time

class Sensors:
    s = SenseHat()

if __name__ == '__main__':
    s = SenseHat()
    s.set_rotation(270)
    while(True):
        north = s.get_compass()
        print("North: %s" % north)
        #time.sleep(0.1)

    