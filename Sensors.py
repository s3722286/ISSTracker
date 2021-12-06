#!/usr/bin/env python3
from sense_hat import SenseHat
import time

class Sensors:
    s = SenseHat()

if __name__ == '__main__':
    s = SenseHat()
    s.set_rotation(270)
    s.set_imu_config(False, True, True)
    
    while(True):
        orientation = s.get_orientation_degrees()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
        time.sleep(0.1)

    