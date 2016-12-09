# position.py
'''
This file holds the information for the position task.
'''

import math
import imu
import pyb

class EncoderTask(object):
    '''
    '''

    def runInt(self, intStuff):
        curA = self.pinA.value()
        curB = self.pinB.value()
        if (curA != self.prevA) == (curB != self.prevB):
            self.errors += 1
        elif self.prevA == curB:
            self.count += 1
        else:
            self.count -= 1
        self.prevA = curA
        self.prevB = curB

    def __init__(self, _pinA, _pinB):
        self.count = 0
        self.errors = 0
        self.prevA = 0
        self.prevB = 0
        self.pinA = _pinA
        self.pinB = _pinB

        self.intA = pyb.ExtInt(_pinA, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, self.runInt)
        self.intB = pyb.ExtInt(_pinB, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, self.runInt)
    
if __name__ == '__main__':
    pass



