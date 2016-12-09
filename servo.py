# servo.py
'''
This file holds all information regarding the servo task and driver object.
'''

import pyb

'''
class ServoTask(object):
    
    def __init__(self, servoPin, offset = 0):
        self.prevServoAngle = 0
        self.servoAngle = 0
        self.angleSpeed = 1 #temporary
        self.atAngle = False
        
        self.servo = Servo.Servo(servoPin, offset)
        return
    
    def run():
        angleChange = abs(servoAngle - prevServoAngle)
        self.transitTime = angleChangle / self.angleSpeed
        self.servo.setAngle()
        return
'''
class Servo(object):
    '''
    '''
    
    def __init__(self, servoPin, offset = 0):
        self.servo = pyb.Servo(servoPin)
        self.offset = offset
        self.angle = 0
        return
    
    def setAngle(self, angle):
        newAngle = self.coerce(0.0, 180.0, (angle - self.offset))
        self.servo.angle(newAngle)
        self.angle = newAngle + self.offset
        return
    
    def coerce(self, minVal, maxVal, val):
        if val < minVal:
            return minVal
        if val > maxVal:
            return maxVal
        return val
    
if __name__ == '__main__':
    print('Running Test Code for: servo.py ... But nothing happened')
