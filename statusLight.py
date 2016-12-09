# position.py
'''
This file holds the information for the position task.
'''

import pyb
import math

class StatusLightTask(object):
    '''
    '''
    
    r = 0
    g = 0
    b = 0
    rNew = 0
    gNew = 0
    bNew = 0

    def __init__(self, _pinR, _pinG, _pinB):

        self.rTimer = pyb.Timer(1, freq = 1000)
        self.rPWM = self.rTimer.channel(1, pyb.Timer.PWM_INVERTED, pin = _pinR)
        self.rPWM.pulse_width_percent(0)

        self.gTimer = pyb.Timer(1, freq = 1000)
        self.gPWM = self.rTimer.channel(2, pyb.Timer.PWM_INVERTED, pin = _pinG)
        self.gPWM.pulse_width_percent(0)

        self.bTimer = pyb.Timer(1, freq = 1000)
        self.bPWM = self.rTimer.channel(3, pyb.Timer.PWM_INVERTED, pin = _pinB)
        self.bPWM.pulse_width_percent(0)

        return

    def run(self):
        self.r += int(math.ceil((self.rNew - self.r)/20))
        self.g += int(math.ceil((self.gNew - self.g)/20))
        self.b += int(math.ceil((self.bNew - self.b)/20))
        self.rPWM.pulse_width_percent(self.r)
        self.gPWM.pulse_width_percent(self.g)
        self.bPWM.pulse_width_percent(self.b)



