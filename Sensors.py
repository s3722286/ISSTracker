#!/usr/bin/env python3
from sense_hat import SenseHat
import time

class Sensors:
    def __init__(self, SenseHat):
        self.s = SenseHat
        self.s.set_imu_config(True, True, True)

    #Note modify yaw to compensate for magnetic/real north mismatch
    def getOrientation(self):
        return self.s.get_orientation_degrees()

if __name__ == '__main__':
    s = SenseHat()
    S = Sensors(s)

    while(True):
        orientation = S.getOrientation()
        print("p: {pitch:.2f}, r: {roll:.2f}, y: {yaw:.2f}".format(**orientation))
        time.sleep(0.1)

    