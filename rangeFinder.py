# rangeFinder.py
'''
This file holds all information regarding the RangeFinder object.
'''

import pyb

class RangeFinder(object):
    
    def __init__(self, rangeFinderPin, cal):
        ''' Calibration: Distance [m] = a + b /( V + k ) , cal [ a b k ]'''
        self.adc = pyb.ADC(rangeFinderPin)
        self.cal = cal
        return

    def getDistance(self):
        ''' Returns distance from sensor [in] '''
        return self.cal[0] + self.cal[1]/(self.adc.read()/819.0 + self.cal[2])
    
if __name__ == '__main__':
    print('Running Test Code for: RangeFinder.py ... But nothing happened')