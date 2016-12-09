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
    # v = [0, 0]

    pos = {
        "x": 0,
        "y": 0,
        "z": 0,
        "heading": 0,
        "roll": 0,
        "pitch": 0,
        }

    def __init__(self, _encoder):
        # Set up encoder.
        self.bno = imu.BNO055()
        self.bno.begin()
        self.lastTime = pyb.millis()
        self.encoder = _encoder
        return

    def run(self):
        countsPerInch = 600.0

        newTime = pyb.millis()
        t = (newTime - self.lastTime)/1000.0
        self.lastTime = newTime

        ang = self.bno.read_euler()


        # acc = self.bno.read_accelerometer()

        # self.a = [
        #     acc[0] * math.cos(math.radians(ang[0])) + acc[1] * math.sin(math.radians(ang[1])),
        #     acc[1] * math.cos(math.radians(ang[0])) + acc[0] * math.sin(math.radians(ang[1])),
        # ]

        # self.v[0] += self.a[0] * t
        # self.v[1] += self.a[1] * t

        v = self.encoder.count/(t * countsPerInch)
        self.encoder.count = 0

        self.pos["x"] += v * math.cos(math.radians(ang[0]))
        self.pos["y"] += v * math.sin(math.radians(ang[0]))

        self.pos["heading"] = ang[0]
        self.pos["roll"] = ang[1]
        self.pos["pitch"] = ang[2]
    
if __name__ == '__main__':
    positionTask = PositionTask()
    positionTask.run()
    print(positionTask.pos())



