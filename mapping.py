
#******************file*****************

import array
import math

class mapObj(object):
    '''
    Creates and adds anylzed sensor data to the map data. 
    '''

    def __init__(self,mapheight, mapWidth, resolution, mapState):
        '''
        Creates the map first time map is run and ajusts the array size (lenght and width) in the case that they are not interger values.
        '''
        print('initializing')
        #Determines the number of elements in array
        self.arrayLength = int(mapheight/resolution)
        self.arrayWidth = int(mapWidth/resolution)
        self.arrayElements = self.arrayLength*self.arrayWidth
        print('self.arrayElements',self.arrayElements)
        self.middleElement = round(self.arrayElements/2+self.arrayWidth/2)
        print(self.middleElement)
        
        #Ensure that if map/length was not an interger the true map size is returned
        self.mapheight = self.arrayLength*resolution
        self.mapHeight = self.arrayWidth*resolution
        
        #defines the byte array
        self.map = bytearray(self.arrayElements)
        
        
        print('init Success\n')
        return

    def mapTask (self,scan):
        '''
        Creates and addes anylzed sensor data to the map data
        '''
        print('mapTask')
        print(self.map)
        self.writemap(scan)
        return

    
    def writemap(self,scan):
        '''
        
        '''
        #print(scan.posX[-1])
        
        print('writemap\n')
        
        self.exitFlag = 0
        while self.exitFlag == 0:
            self.sensorDataLenght = len(scan.posX)
            if  self.sensorDataLenght != 0:
                
                #Sensor_data_curr = Sensor_data[-1] #takes last point in sensor data
                #Sensor_data.pop(-1) # Removes the Sensor_data_curr point from list Sensor_data
                
                self.posX = scan.posX[-1] 
                scan.posX.pop()
                self.posY = scan.posY[-1]
                scan.posY.pop()
                self.headingPlusServoAngle = scan.headingPlusServoAngle[-1] #global angle
                scan.headingPlusServoAngle.pop()
                self.distance = scan.distance[-1] #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
                scan.distance.pop()
                #self.distanceRight = scan.distanceRight[-1]
                #scan.distanceRight.pop()
                
                
                self.dataX = self.posX + self.distance*math.cos(self.headingPlusServoAngle)
                self.dataX = float(format(self.dataX, '.4f')) #**********This tries to eliminate as many duplicate enteries as possible by rounding******
                self.dataY = self.posY + self.distance*math.sin(self.headingPlusServoAngle)
                self.dataY = float(format(self.dataY, '.4f'))
                
                self.newDataPt = [self.dataX,self.dataY]
                print('new point',self.newDataPt)
                self.newDataPtStep = [(self.dataX/resolution),(self.dataY/resolution)]
                print('point in steps',self.newDataPtStep)
                self.newDataPtStep = [round(self.dataX/resolution),round(self.dataY/resolution)]
                print('point in steps rounded',self.newDataPtStep)
                
                #check that x is not greater than difference between map edge and current position 
                
                self.numberRowAboveOrgin = (self.arrayElements/2)/self.arrayWidth
                self.numberRowBlowOrgin = self.numberRowAboveOrgin - 1
                self.numberColumnLeft = self.arrayWidth/2-1
                self.numberColumnRight = self.arrayWidth/2
                
                if self.newDataPtStep[1] > self.numberRowAboveOrgin: #ensures point within 'Northern' bound
                    print('Out of map range Y upper!!!!!!!')
                    print('numberRowAboveOrgin',self.numberRowAboveOrgin)
                elif self.newDataPtStep[1] < -self.numberRowBlowOrgin:  #ensures point within 'Southern' bound
                    print('Out of map range Y lower!!!!!!!')
                    print('numberRowBelowOrgin',self.numberRowBlowOrgin)
                elif self.newDataPtStep[0] > self.numberColumnRight: #ensures point within 'Eastern' bound
                    print('Out of map range X upper!!!!!!!')
                    print('numberColumnRight',self.numberColumnRight)
                elif self.newDataPtStep[0] < -self.numberColumnLeft: #ensures point within 'Western' bound
                    print('Out of map range X lower!!!!!!!')
                    print('numberColumnLeft',self.numberColumnLeft)
                else:
                    self.map[self.middleElement+self.newDataPtStep[0]-self.newDataPtStep[1]*self.arrayWidth]=1
                
                
                print('\n')
                #print(self.map)
            else:
                self.exitFlag = 1
                print(self.map)
                
                print('finished loop')
            
        
        
        
        print('writemap Success\n')
        return 

    #*********Testing*************
    
    def readPoint (x,y):
        '''
        '''

if __name__ == '__main__':        
    #***********Test code**************

    mapheight = 10 #meters (height) Ensure whole numbers 20X20,10x10 I want to avoid 21x21 elements if you choose 10.5
    mapWidth =  10 #meters (witth)
    resolution = .5 #meters Even fraction
    mapState = 0
    
    
    
    class scan():
        print('scan Object created')
    
    scan.posX=array.array('d',[1,2,1,5,5.5,-4.5,-5,0,0,0,0])
    
    scan.posY=array.array('d',[1,1,2,0,0,0,0,0,5,5.5,-4.5,-5])
    
    scan.headingPlusServoAngle=array.array('d',[-33,-33,-33,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing. 
    
    scan.distance=array.array('d',[1,1,1,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
    
            
    testmap = mapObj(mapheight, mapWidth, resolution,mapState)
    testmap.mapTask(scan)
    print('finished mapTask look above matrix to see it in action.  I am currently testing the matrix limits with the points at bound of a 10 meter matrix. I will remove prints later and improve comments.')
    
    
    
