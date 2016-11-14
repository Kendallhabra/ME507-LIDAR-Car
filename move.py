# move.py
'''
This file holds all information regarding the movement task
'''

class moveObj(object):
    '''
    '''
    
    def __init__( self ):
        print( 'Intializing!' )
        #setup servo controller
        print( 'Setup Servo Controller!' )
        #setup motor controller
        print( 'Setup Motor Controller!' )
        return
    
    def moveTask( self , nav = None ): #, new servo angle , new motor speed ):
        print("Movement Task is called from Main")
        if nav is not None:
            servo = nav.servo
            motor = nav.motor
        else:
            servo = 100
            motor = 20
        self.setServo( servo )
        self.setMotor( motor )
        return

    def setServo( self, servo ):
        #set servo angle
        print( 'Setting Servo Angle!' , servo )
    
    def setMotor( self, motor ):
        #set motor speed
        print( 'Setting Motor Speed!' , motor )
        return
    
    
if __name__ == '__main__':
    
    print( 'Running Test Code for: move.py' )
    thing = moveObj()
    thing.moveTask()