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
        if (curA != self.prevA) and (curB != self.prevB):
            # if both pins change --> error
            self.errors += 1
        elif (curA == self.prevA) and (curB == self.prevB):
            # if neither pin changed --> error (shouldnt ever come to this)
            self.errors += 1
        elif self.prevA == curB:
            self.count += 1
        else:
            self.count -= 1
        self.prevA = curA
        self.prevB = curB
        #print('i.',self.count)

    def __init__(self, _pinA, _pinB):
        #print('init encoderTask')
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


