# rangeFinder.py
'''
This file holds all information regarding the RangeFinder object.
'''

class RangeFinder(object):
    '''
    '''
    
    def __init__(self, rangeFinderPin, cal):
        self.adc = pyb.ADC(rangeFinderPin)
        return
    
    def getRaw(self):
        pass

    def getDistance(self):
        val = self.adc.read()
        
    
if __name__ == '__main__':
    print('Running Test Code for: motor.py')