# rangeFinder.py
'''
This file holds all information regarding the RangeFinder object.
'''

import pyb

class RangeFinder(object):
    
    def __init__(self, rangeFinderPin, cal):
        self.adc = pyb.ADC(rangeFinderPin)
        ''' Calibration: Distance [m] = a + b /( V + k ) , cal [ a b k ]'''
        self.cal = cal
        return
    
    def getRaw(self):
        ''' returns adc reading from sensor [V] '''
        return self.adc.read() * 3.3 / (2^12)

    def getDistance(self):
        ''' Returns distance from sensor [m] '''
        return cal[0] + cal[1] /( self.getRaw() + cal[2] )
    
if __name__ == '__main__':
    print('Running Test Code for: RangeFinder.py ... But nothing happened')