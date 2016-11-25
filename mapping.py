#Zachary Arnott
#******************file*****************

import array
import math

class mapObj(object):
    '''
    Creates and adds anylzed sensor data to the map data. It stores in in the class as self.map and can read the map with readPoint()
    '''

    def __init__(self,mapHeight, mapWidth, resolution):
        '''
        Creates the map first time map is run and ajusts the array size (lenght and width) in the case that they are not interger values.
        '''
        
        print('Initializing mapTask.....')
        #Determines the number of elements in array
        self.arrayLength = int(mapHeight/resolution)
        self.arrayWidth = int(mapWidth/resolution)
        self.arrayElements = self.arrayLength*self.arrayWidth
        if self.arrayElements%2 !=0 or self.arrayLength%2 !=0 or self.arrayWidth%2 !=0:
            print('Warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(' * Number of elements in a row and column must be even!!!!!!!!!!!!!')
            print(' * Number of elements in array must be even!!!!!!!!!!!!!!!!!!!!!!!!')
            
        print('arrayElements',self.arrayElements)
        print('arrayWidth',self.arrayWidth)
        print('arrayLength',self.arrayLength)
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
        
        iterTop = 0
        while iterTop < self.arrayWidth:
            '''
            adds a map object boundary on first and last row so robot does not go off the map
            '''
            self.map[iterTop] = 1
            
            self.map[self.arrayElements-self.arrayWidth+iterTop] = 1
            iterTop +=1
            
        self.numberRows = self.arrayElements/self.arrayWidth
        rowIter = 1
        while rowIter < self.numberRows:
            '''
            adds object to first and last column so robot does not go off the map
            '''
            self.map[rowIter*self.arrayWidth] = 1
            self.map[rowIter*self.arrayWidth +self.arrayWidth-1] = 1
            rowIter +=1

        return

    def mapTask (self,scanMain):
        '''
        Creates and addes anylzed sensor data to the map data
        '''
        #print('mapTask')
        #self.printMap()
        self.writemap(scanMain)
        return

    
    def writemap(self,scanMain):
        '''
        This function takes all scanMain data and addes it to the map
        '''
        
        self.exitFlag = 0
        while self.exitFlag == 0:
            '''
            In the event that the following if loop needs to be stopped and memory allocated to other taskes the flag can be changed to 1 thus exiting
            '''
            self.sensorDataLenght = len(scanMain.posX)
            if  self.sensorDataLenght != 0:
                '''
                Iterates through all of the scanMain data until it has all been addaed to the map
                '''
                
                #popping the last data set
                self.posX = scanMain.posX[-1] 
                scanMain.posX.pop()
                self.posY = scanMain.posY[-1]
                scanMain.posY.pop()
                self.headingPlusServoAngle = scanMain.headingPlusServoAngle[-1] #global angle
                scanMain.headingPlusServoAngle.pop()
                self.distance = scanMain.distance[-1] #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
                scanMain.distance.pop()
    
                #Anylsising data and creating data point 
                self.dataX = self.posX + self.distance*math.cos(self.headingPlusServoAngle)
                self.dataX = float(format(self.dataX, '.4f')) #**********This tries to eliminate as many duplicate enteries as possible by rounding******
                self.dataY = self.posY + self.distance*math.sin(self.headingPlusServoAngle)
                self.dataY = float(format(self.dataY, '.4f'))
                
                self.newDataPt = [self.dataX,self.dataY]
                #print('new point',self.newDataPt)
                self.newDataPtStep = [(self.dataX/self.resolution),(self.dataY/self.resolution)]
                #print('point in steps',self.newDataPtStep)
                self.newDataPtStep = [round(self.dataX/self.resolution),round(self.dataY/self.resolution)]
                #print('point in steps rounded',self.newDataPtStep)
                
                #check that x is not greater than difference between map edge and current position 
                
                self.numberRowAboveOrgin = (self.arrayElements/2)/self.arrayWidth
                self.numberRowBlowOrgin = self.numberRowAboveOrgin - 1
                self.numberColumnLeft = self.arrayWidth/2-1
                self.numberColumnRight = self.arrayWidth/2
                
                if self.newDataPtStep[1] > self.numberRowAboveOrgin: #ensures point within 'Northern' bound
                    '''
                    Each of these condition prevents error due to points that are off the map
                    '''
                    print('\n(writeMap Warning) scanMain point Out of map range Y upper!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberRowAboveOrgin',self.numberRowAboveOrgin)
                elif self.newDataPtStep[1] < -self.numberRowBlowOrgin:  #ensures point within 'Southern' bound
                    print('\n(writeMap Warning) scanMain point Out of map range Y lower!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberRowBelowOrgin',self.numberRowBlowOrgin)
                elif self.newDataPtStep[0] > self.numberColumnRight: #ensures point within 'Eastern' bound
                    print('\n(writeMap Warning) scanMain point Out of map range X upper!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberColumnRight',self.numberColumnRight)
                elif self.newDataPtStep[0] < -self.numberColumnLeft: #ensures point within 'Western' bound
                    print('\n(writeMap Warning) scanMain point Out of map range X lower!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberColumnLeft',self.numberColumnLeft)
                else:
                    '''
                    If the point is on the map it is added to map
                    '''
                    self.map[self.middleElement-1+self.newDataPtStep[0]-self.newDataPtStep[1]*self.arrayWidth]=1
            else:
                self.exitFlag = 1
        return 
    
    def readPointXY(self,x,y):
        '''
        Reads a specified coordinate
        '''
        self.newDataRead = [round(x/self.resolution),round(y/self.resolution)]
        
        if self.newDataRead[1] > self.numberRowAboveOrgin: #ensures point within 'Northern' bound
            '''
            Each of these condition prevents error due to points that are off the map
            '''           
            print('\n(readPoint Warning) readPoint Out of map range Y upper, assume wall!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberRowAboveOrgin',self.numberRowAboveOrgin,'\n')
            value = 1 #We can't go off the map so we assume its an object to prevent nav from doing otherwise
        elif self.newDataRead[1] < -self.numberRowBlowOrgin:  #ensures point within 'Southern' bound
            print('\n(readPoint Warning) readPoint Out of map range Y lower, assume wall!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberRowBelowOrgin',self.numberRowBlowOrgin,'\n')
            value = 1 
        elif self.newDataRead[0] > self.numberColumnRight: #ensures point within 'Eastern' bound
            print('\n(readPoint Warning) readPoint Out of map range X upper, assume wall!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberColumnRight',self.numberColumnRight,'\n')
            value = 1
        elif self.newDataRead[0] < -self.numberColumnLeft: #ensures point within 'Western' bound
            print('\n(readPoint Warning) readPoint Out of map range X lower, assume wall!!!!!!!!!!!!!')
            print('Point in steps',self.newDataRead)
            print('numberColumnLeft',self.numberColumnLeft,'\n')
            value = 1
        else:
            '''
            If the point is on the map it is set to value and returned
            '''
            value = self.map[self.middleElement-1+self.newDataRead[0]-self.newDataRead[1]*self.arrayWidth] #-1 because count from 0 no du 
            #print('Bit: ',value)
            
        return value
        
    def printMap(self,dictionary): #!!!!!!!!!!!!may not work in micro python!!!!!!!!!!!!!!!!!!
        '''
        Prints the Map in the best readable formate I have found so far without 3rd party modules
        '''
        print('\n********************Printing map*********************\n')
        print('Map width:',round(self.arrayWidth*self.resolution,1),'m Map Length:', round(self.arrayLength*self.resolution,1),'m Resolution', round(self.resolution,4),'m\n')
        print('Map width:',round(self.arrayWidth*self.resolution*3.28,1),'ft Map Length:', round(self.arrayLength*self.resolution*3.28,1),'ft Resolution', round(self.resolution*3.28,4),'ft\n')
        print('Extremes array units(bitmap units): \n(',-self.numberColumnLeft,self.numberRowAboveOrgin,') (',self.numberColumnRight,self.numberRowAboveOrgin,') (',self.numberColumnRight,-self.numberRowBlowOrgin,') (',-self.numberColumnLeft,-self.numberRowBlowOrgin,')\n')
        print('Extremes in meters:\n(',round(-self.numberColumnLeft*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),') (',round(-self.numberColumnLeft*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),')\n')
        print('Extremes in feet:\n(',round(-self.numberColumnLeft*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),') (',round(-self.numberColumnLeft*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),')\n')
        
        self.iterateCol = 0
        self.iterateRow = 0
        exitFlag = 0
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            if self.arrayElements - (dictionary['positionX']*-1+self.arrayWidth/2 + 1 + (dictionary['positionY']+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
                '''
                If the Robot is the current data point then it prints the robot character '*'
                '''
                print('*', end="")
            else:
                print(self.map[self.iterateRow*self.arrayLength+self.iterateCol], end="")#printing a single bit
            self.iterateCol +=1
            
            if (self.iterateRow+1)*(self.iterateCol) == self.arrayElements:
                '''
                If map complete we exit
                '''
                exitFlag = 1
            elif self.iterateCol == self.arrayWidth:
                '''
                otherwise if the end of a row has been reached we move to the next row
                '''
                self.iterateRow +=1 
                self.iterateCol = 0
                print(end="\n")
        print('\n')
        return   
        
    def printMapFancy(self,dictionary,fill=0,legend=1): #!!!!!!!!!!!!may not work in micro python!!!!!!!!!!!!!!!!!!
        '''
        Prints the Map in the best readable formate I have found so far without 3rd party modules
        '''
        if legend == 1:
            print('\n********************Printing map*********************\n')
            print('Map width:',round(self.arrayWidth*self.resolution,1),'m Map Length:', round(self.arrayLength*self.resolution,1),'m Resolution', round(self.resolution,4),'m\n')
            print('Map width:',round(self.arrayWidth*self.resolution*3.28,1),'ft Map Length:', round(self.arrayLength*self.resolution*3.28,1),'ft Resolution', round(self.resolution*3.28,4),'ft\n')
            print('Extremes array units(bitmap units): \n(',-self.numberColumnLeft,self.numberRowAboveOrgin,') (',self.numberColumnRight,self.numberRowAboveOrgin,') (',self.numberColumnRight,-self.numberRowBlowOrgin,') (',-self.numberColumnLeft,-self.numberRowBlowOrgin,')\n')
            print('Extremes in meters:\n(',round(-self.numberColumnLeft*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),') (',round(-self.numberColumnLeft*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),')\n')
            print('Extremes in feet:\n(',round(-self.numberColumnLeft*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),') (',round(-self.numberColumnLeft*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),')\n')

        if fill == 1:
            '''
            Based on the input the fill type is selected
            '''
            self.fillType = '0'
            self.emptyType = ' '
            self.robot = '*'
        else:
            self.fillType = ' '
            self.emptyType = '0'
            self.robot = '*'
        if legend == 1:
            print('Legend: Robot - * ,','Object - ',self.emptyType,', Empty Space if applicable - ',self.fillType)
        self.iterateCol = 0
        self.iterateRow = 0
        exitFlag = 0
        iter = 0
        while iter < self.arrayWidth:
            '''
            Prints map boarder
            '''
            print('*',end="")
            iter +=1
        print(end='\n')
        
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            if self.arrayElements - (round(dictionary['positionX']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['positionY']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
                print(self.robot, end="")
            elif self.map[self.iterateRow*self.arrayLength+self.iterateCol] == 1:
                print(self.emptyType, end="")#printing a single bit

            else:
                print(self.fillType,end="")
            self.iterateCol +=1
            
            if (self.iterateRow+1)*(self.iterateCol) == self.arrayElements:#If map complete we exit
                exitFlag = 1
            elif self.iterateCol == self.arrayWidth:#otherwise if the end of a row has been reached we move to the next row
                self.iterateRow +=1 
                self.iterateCol = 0
                print(end="*\n")
                
        iter = 0
        print(end='*\n')
        while iter < self.arrayWidth:
            print('*',end="")
            iter +=1
        print(end='\n')
        return  
        
    def readPoint(self,point):
        '''
        reads map based on bitarray coordinates aka element number
        '''
        try:
            value = self.map[int(point)]
        except IndexError:
            value = 1
       
        return value   
 
#********************************************************************************************************************************************************************************
#                                                Test code
#********************************************************************************************************************************************************************************

if __name__ == '__main__':        
    #don't Change or it will messup current validation based on array size
    mapHeight = 30       # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  30       # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .302*.5 # .302#Test with .5 #meters Even fraction Note: see previous note 
    
#Test scanMain array********************************************************
    class scanMain():
        print('scanMain Object created')
        
#Dictionary for lookup of location
    dictionary = {'positionX': 7, 'positionY':5}
    
    ''' use if you need to check orgin location
    scanMain.posX=array.array('f',[10,10,10,10,10,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0])
    scanMain.posY=array.array('f',[9,8,7,6,5,4,3,2,1,0,-1,9,8,7,6,5,4,3,2,1,0,-1])    
    scanMain.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scanMain.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
    '''
    
    scanMain.posX=array.array('f',[1,2,1,5,5.5,-4.5,-5,0,0,0,0,1,0,-1,0,.5,0,-.5,0,10,-9.6])
    scanMain.posY=array.array('f',[1,1,2,0,0,0,0,0,5,5.5,-4.5,-5,0,1,0,-1,0,.5,0,-.5,10,-9.6])    
    scanMain.headingPlusServoAngle=array.array('f',[-33,-33,-33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scanMain.distance=array.array('f',[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.

    #create test map
    mapMain = mapObj(mapHeight, mapWidth, resolution) 
    #Test run mapTask()
    mapMain.mapTask(scanMain)
    #Print Map 
    
    mapMain.printMap(dictionary)
    
    #Testing readPoint    
    print('Testing readPoint')    
    a = mapMain.readPointXY(0,5)
    print('(0,5) bit:',a,'\n')    
    a = mapMain.readPointXY(5,0)
    print('(5,0) bit:',a,'\n')    
    a= mapMain.readPointXY(0,0)
    print('(0,0) bit:',a,'\n')    
    a= mapMain.readPointXY(0,5.5)
    print('(0,5.5) bit:',a)
    #fancy Map test type = 0
    mapMain.printMapFancy(dictionary,0)
