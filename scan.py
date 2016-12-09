# scan.py
'''
This file holds all information regarding the sensors and scanning
'''
import array

class ScanTask(object):
    '''
    '''
    
    def __init__( self ):
        self.posX = array.array('f')
        self.posY = array.array('f')
        self.headingPlusServoAngle = array.array('f')
        self.distance = array.array('f')
        
        self.sensorOffset = array.array('f', [ -45 , -45 , 45 , 45 ] ) # Angle of each sensor wrt servo [deg]
        self.servo = Servo.Servo( 1, offset = 0)
        self.angles = array.array('f', [-90, 90, 15] ) # start angle, max angle, inc angle
        self.servoWait = 50 # ms of wait time for servo to reach new angle
        
        # Create rangeFinder driver objects 
        RF_dict = {
            0 : RF_L1 = rangeFinder.rangeFinder( pin_L1 , cal_L1 ),
            1 : RF_L2 = rangeFinder.rangeFinder( pin_L2 , cal_L2 ),
            2 : RF_R1 = rangeFinder.rangeFinder( pin_R1 , cal_R1 ),
            3 : RF_R2 = rangeFinder.rangeFinder( pin_R2 , cal_R2 )
        }
        
        self.servo.setAngle(self.angles[0])
        self.runTime = pyb.millis() + self.servoWait
        
        return
    
    def run( self ):
        
        if pyb.millis > self.runTime:
            for sensor in range(4):
                self.posX.append( position.pos['x'] )
                self.posY.append( position.pos['y'] )
                self.headingPlusServoAngle.append( position.pos['heading'] + servo.angle + self.sensorOffset[ servo ] )
                self.distance.append( self.RF_dict[ sensor ].getDistance() )
            
            if self.servo.angle < self.angles[1]:
                self.servo.setAngle( self.servo.angle + self.angles[2] )
            else:
                self.servo.setAngle( self.angles[0] )
                
            self.runTime = pyb.millis() + self.servoWait
        
        else:
            pass
        
        return
    
    
if __name__ == '__main__':
    
    print( 'Running Test Code for: scan.py' )