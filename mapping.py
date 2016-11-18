#Zachary Arnott
#******************file*****************

import array
import math
import re #For may print only


class mapObj(object):
    '''
    Creates and adds anylzed sensor data to the map data. It stores in in the class as self.map and can read the map with readPoint()
    '''

    def __init__(self,mapheight, mapWidth, resolution):
        '''
        Creates the map first time map is run and ajusts the array size (lenght and width) in the case that they are not interger values.
        '''
        print('Initializing mapTask.....')
        #Determines the number of elements in array
        self.arrayLength = int(mapheight/resolution)
        self.arrayWidth = int(mapWidth/resolution)
        self.arrayElements = self.arrayLength*self.arrayWidth
        print('self.arrayElements',self.arrayElements)
        self.middleElement = round(self.arrayElements/2+self.arrayWidth/2)
        print('self.middleElement',self.middleElement,'\n')
        
        #Ensure that if map/length was not an interger the true map size is returned
        self.mapHeight = self.arrayLength*resolution
        self.mapWidth = self.arrayWidth*resolution
        self.resolution = resolution
        #defines the byte array
        self.map = bytearray(self.arrayElements)
        
        #Defines obstical array
        self.obsXCoord = array.array('d')
        self.obsYCoord = array.array('d')
        #print('init Success\n')
        return

    def mapTask (self,scan):
        '''
        Creates and addes anylzed sensor data to the map data
        '''
        #print('mapTask')
        #self.printMap()
        self.writemap(scan)
        return

    
    def writemap(self,scan):
        '''
        This function takes all scan data and addes it to the map
        '''
        #print(scan.posX[-1])
        
        #print('\n\nwritemap is being run be mapTask\n')
        
        self.exitFlag = 0
        while self.exitFlag == 0:
            '''
            In the event that the following if loop needs to be stopped and memory allocated to other taskes the flag can be changed to 1 thus exiting
            '''
            self.sensorDataLenght = len(scan.posX)
            if  self.sensorDataLenght != 0:
                '''
                Iterates through all of the scan data until it has all been addaed to the map
                '''
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
                #print('new point',self.newDataPt)
                self.newDataPtStep = [(self.dataX/resolution),(self.dataY/resolution)]
                #print('point in steps',self.newDataPtStep)
                self.newDataPtStep = [round(self.dataX/resolution),round(self.dataY/resolution)]
                #print('point in steps rounded',self.newDataPtStep)
                
                #check that x is not greater than difference between map edge and current position 
                
                self.numberRowAboveOrgin = (self.arrayElements/2)/self.arrayWidth
                self.numberRowBlowOrgin = self.numberRowAboveOrgin - 1
                self.numberColumnLeft = self.arrayWidth/2-1
                self.numberColumnRight = self.arrayWidth/2
                
                if self.newDataPtStep[1] > self.numberRowAboveOrgin: #ensures point within 'Northern' bound
                    print('\n(writeMap Warning) Scan point Out of map range Y upper!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberRowAboveOrgin',self.numberRowAboveOrgin)
                elif self.newDataPtStep[1] < -self.numberRowBlowOrgin:  #ensures point within 'Southern' bound
                    print('\n(writeMap Warning) Scan point Out of map range Y lower!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberRowBelowOrgin',self.numberRowBlowOrgin)
                elif self.newDataPtStep[0] > self.numberColumnRight: #ensures point within 'Eastern' bound
                    print('\n(writeMap Warning) Scan point Out of map range X upper!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberColumnRight',self.numberColumnRight)
                elif self.newDataPtStep[0] < -self.numberColumnLeft: #ensures point within 'Western' bound
                    print('\n(writeMap Warning) Scan point Out of map range X lower!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberColumnLeft',self.numberColumnLeft)
                else:
                    self.map[self.middleElement-1+self.newDataPtStep[0]-self.newDataPtStep[1]*self.arrayWidth]=1
                
                #print('\n')
                #print(self.map)
            else:
                self.exitFlag = 1
                #print(self.map)
                
                #print('finished loop')
        
        #print('writemap Success\n')
        return 
    
    def readPoint (self,x,y):
        '''
        Reads a specified coordinate
        '''
        self.newDataRead = [round(x/resolution),round(y/resolution)]
        #print('Print',x,',',y)
        
        if self.newDataRead[1] > self.numberRowAboveOrgin: #ensures point within 'Northern' bound
            #print('self.newDataRead',self.newDataRead)
            #print('self.numberRowAboveOrgin',self.numberRowAboveOrgin)            
            print('\n(readPoint Warning) readPoint Out of map range Y upper, assume wall!!!!!!!!!!!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberRowAboveOrgin',self.numberRowAboveOrgin,'\n')
            value = 1 #We can't go off the map so we assume its an object to prevent nav from doing otherwise
        elif self.newDataRead[1] < -self.numberRowBlowOrgin:  #ensures point within 'Southern' bound
            print('\n(readPoint Warning) readPoint Out of map range Y lower, assume wall!!!!!!!!!!!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberRowBelowOrgin',self.numberRowBlowOrgin,'\n')
            value = 1 
        elif self.newDataRead[0] > self.numberColumnRight: #ensures point within 'Eastern' bound
            print('\n(readPoint Warning) readPoint Out of map range X upper, assume wall!!!!!!!!!!!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberColumnRight',self.numberColumnRight,'\n')
            value = 1
        elif self.newDataRead[0] < -self.numberColumnLeft: #ensures point within 'Western' bound
            print('\n(readPoint Warning) readPoint Out of map range X lower, assume wall!!!!!!!!!!!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberColumnLeft',self.numberColumnLeft,'\n')
            value = 1
        else:
            value = self.map[self.middleElement-1+self.newDataRead[0]-self.newDataRead[1]*self.arrayWidth] #-1 because count from 0 no du 
            #print('Bit: ',value)
            
        return value
        
    def printMap(self):
        '''
        Prints the Map in the best readable formate I have found so far without 3rd party modules
        '''
        print('\n********************Printing map*********************\n')
        print('Map width:',self.arrayWidth*resolution,'m Map Length:', self.arrayLength*resolution,'m Resolution', resolution,'m\n')
        print('Extremes array units(bitmap units): \n(',-self.numberColumnLeft,self.numberRowAboveOrgin,') (',self.numberColumnRight,self.numberRowAboveOrgin,') (',self.numberColumnRight,-self.numberRowBlowOrgin,') (',-self.numberColumnLeft,-self.numberRowBlowOrgin,')\n')
        print('Extremes in meters:\n(',-self.numberColumnLeft*resolution,self.numberRowAboveOrgin*resolution,') (',self.numberColumnRight*resolution,self.numberRowAboveOrgin*resolution,') (',self.numberColumnRight*resolution,-self.numberRowBlowOrgin*resolution,') (',-self.numberColumnLeft*resolution,-self.numberRowBlowOrgin*resolution,')\n')
        self.iterator = 1
        while self.iterator <= self.arrayLength:
            rowStart = int(self.arrayWidth*(self.iterator-1))
            rowEnd = int(self.arrayWidth*self.iterator)
            currentMapString = str(testmap.map[rowStart:rowEnd])
            currentMapString = currentMapString.replace("bytearray", "")
            currentMapString = currentMapString.replace("(b'", "")
            currentMapString = currentMapString.replace("')", "")
            currentMapString = currentMapString.replace("x", "")
            #currentMapString = currentMapString[2::3]#attempt to avoid regular expressions 
            #print(currentMapString[1::2],'')
            currentMapString = re.sub('[^\w]', '', currentMapString)
            print(currentMapString[1::2])
            #print(str(testmap.map[rowStart:rowEnd]))
            self.iterator += 1

        return   
            
if __name__ == '__main__':        
    #***********Test code**************
    #don't Change or it will messup current validation based on array size
    mapheight = 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .5 #meters Even fraction Note: see previous note 
    
#Test scan array********************************************************
    class scan():
        print('scan Object created')
    
    scan.posX=array.array('d',[1,2,1,5,5.5,-4.5,-5,0,0,0,0,1,0,-1,0,.5,0,-.5,0])
    scan.posY=array.array('d',[1,1,2,0,0,0,0,0,5,5.5,-4.5,-5,0,1,0,-1,0,.5,0,-.5])    
    scan.headingPlusServoAngle=array.array('d',[-33,-33,-33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scan.distance=array.array('d',[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
    #create test map
    testmap = mapObj(mapheight, mapWidth, resolution) 
    #Test run mapTask()
    testmap.mapTask(scan)
    #Print Map 
    
    testmap.printMap()
    #print('\n\nFinished mapTask look above matrix to see it in action.  I am currently testing the matrix limits \nwith the points at bound of a 10 meter matrix. I will remove prints later and improve comments.')
    print('\n\n')
    
    #Testing readPoint
    print('Testing readPoint')    
    a = testmap.readPoint(0,5)
    print('(0,5) bit:',a,'\n')    
    a = testmap.readPoint(5,0)
    print('(5,0) bit:',a,'\n')    
    a= testmap.readPoint(0,0)
    print('(0,0) bit:',a,'\n')    
    a= testmap.readPoint(0,5.5)
    print('(0,5.5) bit:',a)
    
 
