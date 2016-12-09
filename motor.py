# motor.py
'''
This file holds all information regarding the motor object.  The motor object
includes both a DC motor and a shaft encoder.
'''

class moveObj(object):
    '''
    '''

    direction = 0
    power = 0
    
    def __init__(self, motorPinA, motorPinB):
        self.motorA = pyb.Pin("Motor PWM A", pyb.Pin.OUT_PP)
        self.motorA.value(0)
        return

    def run():
        self.motorA.value(self.direction)


if __name__ == '__main__':
    print('Running Test Code for: motor.py')