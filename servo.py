# servo.py
'''
This file holds all information regarding the servo object.
'''

class Servo(object):
    '''
    '''
    
    def __init__(self, servoPin, offset = 0):
        self.distance = 0
        # Set up encoder.
        return
    
    def setAngle(self, angle):
        newAngle = self.coerce(0.0, 180.0, (angle - self.offset))

        pass

    def setOffset(self, offset):
        pass

    def coerce(self, minVal, maxVal, val):
        if val < minVal:
            return minVal
        if val > maxVal:
            return maxVal
        return val
    
    
if __name__ == '__main__':
    print('Running Test Code for: motor.py')