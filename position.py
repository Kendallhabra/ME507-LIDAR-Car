# position.py
'''
This file holds the information for the position task.
'''

import math
import imu
import pyb

class PositionTask(object):
    '''
    '''
    
    lastTime = 0
    v = [0, 0]

    pos = {
        "x": 0,
        "y": 0,
        "z": 0,
        "heading": 0,
        "roll": 0,
        "pitch": 0,
        }

    def __init__(self):
        # Set up encoder.
        self.bno = imu.BNO055()
        self.bno.begin()
        self.lastTime = pyb.millis()
        return

    def run(self):
        newTime = pyb.millis()
        t = (newTime - self.lastTime)/1000
        self.lastTime = newTime

        ang = self.bno.read_euler()
        newAcc = self.bno.read_accelerometer()

        print(ang[0])
        print(ang[1])
        print(math.radians(ang[0])

        a = [
            acc[0] * math.cos(math.radians(ang[0])) + acc[1] * math.sin(math.radians(ang[1])),
            acc[1] * math.cos(math.radians(ang[0])) + acc[0] * math.sin(math.radians(ang[1])),
        ]

        self.v[0] += a[0]
        self.v[1] += a[1]


        self.pos["x"] += .5 * acc[0] * t * math.cos(math.radians(ang[0])) + .5 * acc[1] * t^2 * math.sin(math.radians(ang[1]))
        print(self.pos["x"])
        self.pos["y"] += .5 * acc[1] * t^2 * math.cos(math.radians(ang[0])) + .5 * acc[0] * t^2 * math.sin(math.radians(ang[1]))

        self.pos["heading"] = ang[0]
        self.pos["roll"] = ang[1]
        self.pos["pitch"] = ang[2]
    
if __name__ == '__main__':
    positionTask = PositionTask()
    positionTask.run()
    print(positionTask.pos())



    