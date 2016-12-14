# scan.py
'''package docstring
This file holds all information regarding the sensors and scanning
'''
import array
import math
import os
if os.getcwd() == '/' or os.getcwd() == '/sd': 
    #allows for testing on computer without modules that can only run on the pyboard
    import servo
    import rangeFinder
    import pyb
    

class ScanTask(object):
    '''
    '''
    global posX
    global posY
    global headingPlusServoAngle
    global distance
    posX = array.array('f')
    posY = array.array('f')
    headingPlusServoAngle = array.array('f')
    distance = array.array('f')
    if os.getcwd() != '/' or os.getcwd() != '/sd': #Testing data for computer only runs if not on pyboard
        posX=array.array('f',[x*.325*.7 for x in [1,2,1,5,5.5,-4.5,-5,0,0,0,0,1,0,-1,0,.5,0,-.5,0,10,-9.6,6,7,10,10,10,10,0,1,12,-10, -10,-11,-12,-10,-10,11,12,13,5,0,0,-10,32,22,30,20,28,26,24,18,16,14,12,10,28,31,26,29,28,0,0,-2,-4,-12,-12,-14,-14,-30,-28,-26,-24,-24,-24,-24,-30,-28,-26,-24,-24,-24,-24,9,7,3,3,10,10,10,9,15,16,17,18,0,-2,-3,-2,0,10,12,14,16]])
        posY=array.array('f',[x*.325*.7 for x in [1,1,2,0,0,0,0,0,5,5.5,-4.5,-5,0,1,0,-1,0,.5,0,-.5,10,-9.6,3,3,10,11,12,10,0,1,0,0,-6,-6,-6,-9,-11,-9,-9,-9,-3,-8,-7,3,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-5,-3,10,12,14,16,18,-3,31,29,31,31,29,31,29,0,0,0,0,2,4,6,-6,-6,-6,-6,-8,-10,-12,1,-3,-3,2,9,7,5,4,30,30,30,30,-30,-29,-27,-25,-24,-31,-29,-27,-25]])    
        headingPlusServoAngle=array.array('f',[-33,-33,-33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
        distance=array.array('f',[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
        
        i = 0
        while i < 0:
            '''
            Ensures angles are being enterpeted correctly by test 0-90 90-180 etc
            '''
            posX.append(0)
            posY.append(0)
            headingPlusServoAngle.append(i)
            distance.append(5)
            i +=1
        
    
    
    def __init__(self, pins, positionTask):
        
        self.position = positionTask
        
        
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
            rangeFinder.RangeFinder( pins["Rangefinder 3"] , [7, 50.0, -1.97] )  # Bottom Right
        ]
        
        self.servo.setAngle(self.angles[0])
        self.runTime = pyb.millis() + self.servoWait

        self.bluetooth = pyb.UART(2, 9600)
        self.bluetooth.init(9600, bits=8, parity=None, stop=1)
        
        return
    
    def run( self ):
        
        if pyb.millis() > self.runTime:
            for i, sensor in enumerate(self.rangeFinders):
                posX.append( self.position.pos['x'] )
                posY.append( self.position.pos['y'] )
                headingPlusServoAngle.append( self.position.pos['heading'] + self.servo.angle + self.sensorOffset[i] )
                distance.append(sensor.getDistance())
            
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
        
        x = posX[-1]
        y = posY[-1]
        h = headingPlusServoAngle[-1]
        r = distance[-1]

        posX = posX[0:-1]
        posY = posY[0:-1]
        headingPlusServoAngle = headingPlusServoAngle[0:-1]
        distance = distance[0:-1]

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
