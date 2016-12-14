# scan.py
'''
This file holds all information regarding the sensors and scanning
'''
import array
import servo
import rangeFinder
import pyb
import math

class ScanTask(object):
    '''
    '''
    
    def __init__(self, pins, positionTask):
        self.position = positionTask
        self.posX = array.array('f')
        self.posY = array.array('f')
        self.headingPlusServoAngle = array.array('f')
        self.distance = array.array('f')
        
        #self.sensorOffset = array.array('f', [ -45 , -45 , 45 , 45 ] ) # Angle of each sensor wrt servo [deg]
        self.sensorOffset = array.array('f', [45 ] ) # Angle of each sensor wrt servo [deg]
        self.servo = servo.Servo( 1, offset = 0)
        self.angles = array.array('f', [-90, 90, 15] ) # start angle, max angle, inc angle
        #self.angles = array.array('f', [0, 0, 15] ) # start angle, max angle, inc angle
        self.servoWait = 200 # ms of wait time for servo to reach new angle
        
        # Create rangeFinder driver objects 
        self.rangeFinders = [
            #rangeFinder.RangeFinder( pins["Rangefinder 4"] , [0, 0, 0] ), # Top Left
            #rangeFinder.RangeFinder( pins["Rangefinder 3"] , [0, 55, -2]), # Bottom Left
            #rangeFinder.RangeFinder( pins["Rangefinder 2"] , [0, 0, 0] ), # Top Right
            # rangeFinder.RangeFinder( pins["Rangefinder 3"] , [7, 50.0, -1.97] )  # Bottom Right
            rangeFinder.RangeFinder( pins["Rangefinder 3"] , [7, 40950.0, 1613.43] )  # Bottom Right
        ]
        
        self.servo.setAngle(self.angles[0])
        self.runTime = pyb.millis() + self.servoWait

        self.bluetooth = pyb.UART(2, 9600)
        self.bluetooth.init(9600, bits=8, parity=None, stop=1)
        
        return
    
    def run( self ):
        
        if pyb.millis() > self.runTime:
            for i, sensor in enumerate(self.rangeFinders):
                self.posX.append( self.position.pos['x'] )
                self.posY.append( self.position.pos['y'] )
                self.headingPlusServoAngle.append( self.position.pos['heading'] + self.servo.angle + self.sensorOffset[i] )
                self.distance.append(sensor.getDistance())
            
            if self.servo.angle < self.angles[1]:
                self.servo.setAngle( self.servo.angle + self.angles[2] )
            else:
                self.servo.setAngle( self.angles[0] )
                
            self.runTime = pyb.millis() + self.servoWait
        
        else:
            pass
        
        return

    def popToSerial( self ):
        if len(self.posX) < 1:
            return
        
        x = self.posX[-1]
        y = self.posY[-1]
        h = self.headingPlusServoAngle[-1]
        r = self.distance[-1]

        self.posX = self.posX[0:-1]
        self.posY = self.posY[0:-1]
        self.headingPlusServoAngle = self.headingPlusServoAngle[0:-1]
        self.distance = self.distance[0:-1]

        x1 = x + r * math.cos(math.radians(h))
        y1 = y + r * math.sin(math.radians(h))
        print("Coords: ",x, y, x1, y1, r, h)

        self.bluetooth.write("<")
        self.bluetooth.write(str(int(x1*5)))
        self.bluetooth.write(",")
        self.bluetooth.write(str(int(y1*5)))
        self.bluetooth.write(",")
        self.bluetooth.write("255")
        self.bluetooth.write(",")
        self.bluetooth.write(str(int(h)))
        self.bluetooth.write(">")
    
    
if __name__ == '__main__':
    
    print( 'Running Test Code for: scan.py' )