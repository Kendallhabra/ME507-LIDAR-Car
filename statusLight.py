# position.py
'''
This file holds the information for the position task.
'''

import pyb

class StatusLightTask(object):
    '''
    '''
    
    r = 0
    g = 0
    b = 0

    def __init__(self, _pinR, _pinG, _pinB):

        self.rTimer = pyb.Timer(1, freq = 1000)
        self.rPWM = self.rTimer.channel(1, pyb.Timer.PWM, pin = _pinR)
        self.rPWM.pulse_width_percent(0)

        self.gTimer = pyb.Timer(1, freq = 1000)
        self.gPWM = self.rTimer.channel(2, pyb.Timer.PWM, pin = _pinG)
        self.gPWM.pulse_width_percent(0)

        self.bTimer = pyb.Timer(1, freq = 1000)
        self.bPWM = self.rTimer.channel(3, pyb.Timer.PWM, pin = _pinB)
        self.bPWM.pulse_width_percent(0)

        self.pinR = pyb.Pin(_pinR, pyb.Pin.OUT_PP)
        self.pinG = pyb.Pin(_pinG, pyb.Pin.OUT_PP)
        self.pinB = pyb.Pin(_pinB, pyb.Pin.OUT_PP)
        self.runs = 0
        return

    def run(self):
        self.rPWM.pulse_width_percent(self.r)
        self.gPWM.pulse_width_percent(self.g)
        self.bPWM.pulse_width_percent(self.b)




