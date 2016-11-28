# position.py
'''
This file holds the information for the position task.
'''

class Position(object):
    '''
    '''
    
    def __init__(self, servoPin, offset = 0):
        self.distance = 0
        # Set up encoder.
        return
    
    def getPosition(self, angle):
        newAngle = self.coerce(0.0, 180.0, (angle - self.offset))

        pass

    def run():
        pass
    
if __name__ == '__main__':
    print('Running Test Code for: motor.py')