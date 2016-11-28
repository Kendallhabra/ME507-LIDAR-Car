# motor.py
'''
This file holds all information regarding the motor object.  The motor object
includes both a DC motor and a shaft encoder.
'''

class moveObj(object):
    '''
    '''
    
    def __init__(self, encPinA, encPinB, motorPinA, motorPinB, motorPinErr, ):
        self.distance = 0
        # Set up encoder.
        return
    
    def setPWM(self, direction, dutyCycle):
        pass

    def getDistance(self):
        pass

    def resetDistance(self):
        pass

    def encoderISR(self):
        pass

    def setBrake(self, brakeStatus):
        pass

    
    
if __name__ == '__main__':
    print('Running Test Code for: motor.py')