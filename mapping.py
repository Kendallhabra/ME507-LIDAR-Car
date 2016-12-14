#Zachary Arnott
#******************file*****************

import array
import math
import os
import scan
import position
if os.getcwd() == '/' or os.getcwd() == '/sd': 
    #allows for testing on computer without modules that can only run on the pyboard
    import pyb
    
    

class mapObj(object):
    '''
    Creates and adds anylzed sensor data to the map data. It stores in in the class as self.map and can read the map with readPoint()
    '''

    def __init__(self,mapHeight, mapWidth, resolution):
        '''
        Creates the map first time map is run and ajusts the array size (lenght and width) in the case that they are not interger values.
        '''
        self.saveMapFlag = 0
        
        
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
        global map
        map = bytearray(self.arrayElements)
        
        #Defines obstical array
        self.obsXCoord = array.array('d')
        self.obsYCoord = array.array('d')
        #print('init Success\n')
        
        iterTop = 0
        while iterTop < self.arrayWidth:
            '''
            adds a map object boundary on first and last row so robot does not go off the map
            '''
            map[iterTop] = 1
            
            map[self.arrayElements-self.arrayWidth+iterTop] = 1
            iterTop +=1
            
        self.numberRows = self.arrayElements/self.arrayWidth
        rowIter = 1
        while rowIter < self.numberRows:
            '''
            adds object to first and last column so robot does not go off the map
            '''
            map[rowIter*self.arrayWidth] = 1
            map[rowIter*self.arrayWidth +self.arrayWidth-1] = 1
            rowIter +=1
        
        self.xyList = []
        
        if __name__ != '__main__' or os.getcwd() == '/':
            self.saveMapInterval = 10000 #ms or 10 seconds till next save
            #self.runTime = pyb.millis() + self.saveMapInterval
        #***************
       

        #****************
        return

    def mapTask (self):
        '''
        Creates and addes anylzed sensor data to the map data
        '''
        #print('mapTask')
        #self.printMap()
        self.writeMap()
        if __name__ != '__main__' or os.getcwd() == '/':
            self.saveMapTimed(1) #1 means it will overwrite last saved map so no backups
        return

    
    def writeMap(self):
        '''
        This function takes all scanTask data and addes it to the map
        '''
        
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
                
                #popping the last data set
                self.posX = scan.posX[-1] 
                scan.posX = scan.posX[0:-1]
                self.posY = scan.posY[-1]
                scan.posY = scan.posY[0:-1]
                self.headingPlusServoAngle = scan.headingPlusServoAngle[-1] #global angle
                scan.headingPlusServoAngle = scan.headingPlusServoAngle[0:-1]
                self.distance = scan.distance[-1] #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
                scan.distance = scan.distance[0:-1]
    
                #Anylsising data and creating data point 
                self.dataX = self.posX + self.distance*math.cos((self.headingPlusServoAngle-90)*-0.0174533)
                self.dataX = float(format(self.dataX, '.4f')) #**********This tries to eliminate as many duplicate enteries as possible by rounding******
                self.dataY = self.posY + self.distance*math.sin((self.headingPlusServoAngle-90)*-0.0174533)
                self.dataY = float(format(self.dataY, '.4f'))
                #<p,dataX,dataY>
                
                #self.xyList.append(['<p,'+str(self.dataX)+','+str(self.dataY)+'>']) #*************************************************************************************************************
                #print(self.xyList)
                
                
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
                    print('\n(writeMap Warning) scanTask point Out of map range Y upper!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberRowAboveOrgin',self.numberRowAboveOrgin)
                elif self.newDataPtStep[1] < -self.numberRowBlowOrgin:  #ensures point within 'Southern' bound
                    print('\n(writeMap Warning) scanTask point Out of map range Y lower!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberRowBelowOrgin',self.numberRowBlowOrgin)
                elif self.newDataPtStep[0] > self.numberColumnRight: #ensures point within 'Eastern' bound
                    print('\n(writeMap Warning) scanTask point Out of map range X upper!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberColumnRight',self.numberColumnRight)
                elif self.newDataPtStep[0] < -self.numberColumnLeft: #ensures point within 'Western' bound
                    print('\n(writeMap Warning) scanTask point Out of map range X lower!!!!!!!!!!!!!!!!!!!!!!!')
                    print('point in steps',self.newDataPtStep)
                    print('numberColumnLeft',self.numberColumnLeft)
                else:
                    '''
                    If the point is on the map it is added to map
                    '''
                    
                    map[self.middleElement-1+self.newDataPtStep[0]-self.newDataPtStep[1]*self.arrayWidth]=1
            else:
                self.exitFlag = 1
        return 
    

    
    def saveMap(self,overWriteFile = 0):
        '''
        Saves the map to a txt file (map#.txt)
        '''
        dictionary = position.pos
        #If code is on pyboard it changes /sd directory
        if __name__ == '__main__'or os.getcwd() != '/':
            pyboardSD = ''
            save_path = os.getcwd()
            
        else:
            pyboardSD = ''
            save_path = os.getcwd()+pyboardSD 

        name_of_file = "Map0"

        i = 1
        #print(os.path.exists(pyboardSD + name_of_file+'.txt'))
        print('Determine new map file name')
        while os.path.exists(pyboardSD + name_of_file+'.txt') == True and overWriteFile==0:
            '''
            If the map exits we index to the next file name 
            '''
            name_of_file = "Map"+str(i)
            #print(name_of_file)
            #print(os.path.exists(pyboardSD + name_of_file+'.txt'))
            i +=1

        print('Writing file '+ name_of_file+'.txt ...')    
        completeName = os.path.join(save_path, name_of_file+".txt")         
        mapFile = open(completeName, "w")

        mapString = '<'+str(self.resolution)+'>'
        self.iterateCol = 0
        self.iterateRow = 0
        exitFlag = 0
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            if self.arrayElements - (round(dictionary['x']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['y']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
                '''
                If the Robot is the current data point then it prints the robot character '*'
                '''
                mapString = mapString+'*'
            else:
                mapString = mapString+str(map[self.iterateRow*self.arrayLength+self.iterateCol])#printing a single bit
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
                mapString = mapString+"\n"
        mapFile.write(mapString)

        mapFile.close()
        print('Done')    
    
    def saveMapTimed(self,overWriteFile = 0,dictionary = False):
        '''
        Saves Map to file on a timer 
        '''
        if pyb.millis() > self.runTime:
        
            #If code is on pyboard it changes /sd directory
            if __name__ == '__main__':
                pyboardSD = ''
                save_path = os.getcwd()
                
            else:
                pyboardSD = ''
                save_path = os.getcwd()+pyboardSD 

            name_of_file = "Map0"

            i = 1
            #print(os.path.exists(pyboardSD + name_of_file+'.txt'))
            print('Determine new map file name')
            while os.path.exists(pyboardSD + name_of_file+'.txt') == True and overWriteFile==1:
                '''
                If the map exits we index to the next file name 
                '''
                name_of_file = "Map"+str(i)
                #print(name_of_file)
                #print(os.path.exists(pyboardSD + name_of_file+'.txt'))
                i +=1

            print('Writing file'+ name_of_file+'.txt ...')    
            completeName = os.path.join(save_path, name_of_file+".txt")
            if save_path == '/sd' or __name__ == '__main__':
                mapFile = open(completeName, "w")

                mapString = '<'+str(self.resolution)+'>'
                self.iterateCol = 0
                self.iterateRow = 0
                exitFlag = 0
                while exitFlag == 0:
                    '''
                    Iterates through each bit printing only the bit with no spaces. 
                    '''
                    if dictionary != False and self.arrayElements - (round(dictionary['x']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['y']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
                        '''
                        If the Robot is the current data point then it prints the robot character '*'
                        '''
                        mapString = mapString+'*'
                    else:
                        mapString = mapString+str(map[self.iterateRow*self.arrayLength+self.iterateCol])#printing a single bit
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
                        mapString = mapString+"\n"
                        
                
                mapFile.write(mapString)

                mapFile.close()
                print('Done') 
            else:
                print('Directory not /sd!!!!!!!!!!!!!')
            self.runTime = pyb.millis() + self.servoWait
        return
    
    
 

        
 
        
        
        
        
        
#********************************************************************************************************************************************************************************
#                                                Test code
#********************************************************************************************************************************************************************************

if __name__ == '__main__':        
    #don't Change or it will messup current validation based on array size
    mapHeight = 15       # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  15       # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .304*.7 # .302#Test with .5 #meters Even fraction Note: see previous note 
    
    #Test scanTask array********************************************************

    #Changing starting location from center of map to a specified point for testing
    position.pos = {'x': 4, 'y':5}
    
    
    
    #create test map
    mappingTask = mapObj(mapHeight, mapWidth, resolution) 
    #Test run mapTask()
    mappingTask.mapTask()
    #Print Map 
    
    
    
    #***********************************************************
    # Test SaveMap commented so it does not spam current directory******************
    #*****************************************************
    mappingTask.saveMap()
    
