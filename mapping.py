#Zachary Arnott
#******************file*****************

import array
import math
import os

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
        
        self.xyList = []
        
        #Create an intial timer count
        if __name__ != '__main__' and os.getcwd() =='/':
            self.saveMapInterval = 10000 #ms or 10 seconds till next save
            self.runTime = pyb.millis() + self.saveMapInterval
        #***************
       

        #****************
        return

    def mapTask (self,scanMain):
        '''
        Creates and addes anylzed sensor data to the map data
        '''
        #print('mapTask')
        #self.printMap()
        self.writeMap(scanMain)
        if __name__ != '__main__' or __name__ =='/':
            self.saveMapTimed(1) #1 means it will overwrite last saved map so no backups
        return

    
    def writeMap(self,scanMain):
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
                #<p,dataX,dataY>
                
                self.xyList.append(['<p,'+str(self.dataX)+','+str(self.dataY)+'>'])
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
            if self.arrayElements - (round(dictionary['x']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['y']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
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
    
    def saveMap(self,overWriteFile = 0,dictionary = False):

        #If code is on pyboard it changes /sd directory
        if __name__ == '__main__'or os.getcwd() != '/':
            pyboardSD = ''
            save_path = os.getcwd()
            
        else:
            pyboardSD = '/sd'
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
                mapString = mapString+str(self.map[self.iterateRow*self.arrayLength+self.iterateCol])#printing a single bit
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
    
        if pyb.millis > self.runTime:
        
            #If code is on pyboard it changes /sd directory
            if __name__ == '__main__':
                pyboardSD = ''
                save_path = os.getcwd()
                
            else:
                pyboardSD = '/sd'
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
                    mapString = mapString+str(self.map[self.iterateRow*self.arrayLength+self.iterateCol])#printing a single bit
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
            self.runTime = pyb.millis() + self.servoWait
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
            if self.arrayElements - (round(dictionary['x']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['y']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
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
    def printMapGUI(self,dictionary): #!!!!!!!!!!!!may not work in micro python!!!!!!!!!!!!!!!!!!
        '''
        Prints the Map in the best readable formate I have found so far without 3rd party modules
        '''
        # print('\n********************Printing map*********************\n')
        # print('Map width:',round(self.arrayWidth*self.resolution,1),'m Map Length:', round(self.arrayLength*self.resolution,1),'m Resolution', round(self.resolution,4),'m\n')
        # print('Map width:',round(self.arrayWidth*self.resolution*3.28,1),'ft Map Length:', round(self.arrayLength*self.resolution*3.28,1),'ft Resolution', round(self.resolution*3.28,4),'ft\n')
        # print('Extremes array units(bitmap units): \n(',-self.numberColumnLeft,self.numberRowAboveOrgin,') (',self.numberColumnRight,self.numberRowAboveOrgin,') (',self.numberColumnRight,-self.numberRowBlowOrgin,') (',-self.numberColumnLeft,-self.numberRowBlowOrgin,')\n')
        # print('Extremes in meters:\n(',round(-self.numberColumnLeft*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),') (',round(-self.numberColumnLeft*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),')\n')
        # print('Extremes in feet:\n(',round(-self.numberColumnLeft*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),') (',round(-self.numberColumnLeft*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),')\n')
        
        import tkinter #import here is pyboard does not try and do this
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root)
        self.canvas.pack()
        self.canvas.config(width=790, height=790)
        
        
        self.iterateCol = 0
        self.iterateRow = 0
        exitFlag = 0
        mapPixels = 4
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            if self.arrayElements - (round(dictionary['x']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['y']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
                '''
                If the Robot is the current data point then it prints the robot character '*'
                '''
                self.rect = self.canvas.create_rectangle(mapPixels*self.iterateCol   ,mapPixels*self.iterateRow   ,   mapPixels*(self.iterateCol+1)   ,   mapPixels*(self.iterateRow +1)  , outline="black", fill="red")
            elif self.map[self.iterateRow*self.arrayLength+self.iterateCol]==1:
                self.rect = self.canvas.create_rectangle(mapPixels*self.iterateCol   ,mapPixels*self.iterateRow   ,   mapPixels*(self.iterateCol+1)   ,   mapPixels*(self.iterateRow +1)  , outline="black", fill="white")
            else:
                
                self.rect = self.canvas.create_rectangle(mapPixels*self.iterateCol   ,mapPixels*self.iterateRow   ,   mapPixels*(self.iterateCol+1)   ,   mapPixels*(self.iterateRow +1)  , outline="black", fill="black")

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
            #self.after(20,printMapGUI) 
            #self.root.update()
        
        return             
        
    def printSavedMap(self): #!!!!!!!!!!!!may not work in micro python!!!!!!!!!!!!!!!!!!
        '''
        Prints the Map in the best readable formate I have found so far without 3rd party modules
        '''
        # print('\n********************Printing map*********************\n')
        # print('Map width:',round(self.arrayWidth*self.resolution,1),'m Map Length:', round(self.arrayLength*self.resolution,1),'m Resolution', round(self.resolution,4),'m\n')
        # print('Map width:',round(self.arrayWidth*self.resolution*3.28,1),'ft Map Length:', round(self.arrayLength*self.resolution*3.28,1),'ft Resolution', round(self.resolution*3.28,4),'ft\n')
        # print('Extremes array units(bitmap units): \n(',-self.numberColumnLeft,self.numberRowAboveOrgin,') (',self.numberColumnRight,self.numberRowAboveOrgin,') (',self.numberColumnRight,-self.numberRowBlowOrgin,') (',-self.numberColumnLeft,-self.numberRowBlowOrgin,')\n')
        # print('Extremes in meters:\n(',round(-self.numberColumnLeft*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(self.numberRowAboveOrgin*self.resolution,1),') (',round(self.numberColumnRight*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),') (',round(-self.numberColumnLeft*self.resolution,1),round(-self.numberRowBlowOrgin*self.resolution,1),')\n')
        # print('Extremes in feet:\n(',round(-self.numberColumnLeft*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(self.numberRowAboveOrgin*self.resolution*3.28,1),') (',round(self.numberColumnRight*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),') (',round(-self.numberColumnLeft*self.resolution*3.28,1),round(-self.numberRowBlowOrgin*self.resolution*3.28,1),')\n')
        Filetrueorfalse = 0
        import re
        while Filetrueorfalse ==0:
            '''Take a file name input from use and check that it exists before continuing and throughs error if it is invalid
            '''
            mapFilename = input("Input Map file name and extention and hit enter to plot(map0.txt): ")#input file name

            if os.path.isfile(mapFilename):#If else checks for file before contining 
                Filetrueorfalse = 1
            else: 
                print(' \n!!!Warning!!! \nFile does not exist in program directory ensure correct name and extention. \nExamples include: name.extention , name.csv , name.txt\n\n')

        with open (mapFilename, "r") as myfile: #Inspired by example in python documentation 
            '''Imports characters from file removes any non-number characters and seperates them into 1 by 2 matrixs
            '''
            mapdata=myfile.read()#imports characters as string for each line
            mapdata = mapdata.split('>')
            resolution = round(float(re.sub("[<]", "",mapdata[0] )),3)
            map = mapdata[1]
            numberOfCol = map.count('\n')+1
            map = re.sub("[\n]", "",map )
            numberOfElements = len(map)
            numberOfRows = int(numberOfElements/numberOfCol)
            print('\n\nOpening ', mapFilename,'...')
            print('Number of Columns', numberOfCol)
            print('Number of Rows',numberOfRows)
            print('Number of Elements', numberOfElements)
            print('Map width:',round(numberOfCol*resolution,1),'m Map Length:', round(numberOfRows*resolution,1),'m Resolution', round(resolution,4),'m')
            print('Map width:',round(numberOfCol*resolution*3.28,1),'ft Map Length:', round(numberOfRows*resolution*3.28,1),'ft Resolution', round(resolution*3.28,4),'ft\n')
        import tkinter #import here is pyboard does not try and do this
        
        mapPixels = 4
        
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root)
        self.canvas.pack()
        self.canvas.config(width=numberOfRows*mapPixels-2, height=numberOfCol*mapPixels-2)
        
        
        self.iterateCol = 0
        self.iterateRow = 0
        exitFlag = 0
        
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            #print('running')
            if   map[self.iterateRow*numberOfCol+self.iterateCol] == '*':
                print('*******************************************')
                '''
                If the Robot is the current data point then it prints the robot character '*'
                '''
                self.rect = self.canvas.create_rectangle(mapPixels*self.iterateCol   ,mapPixels*self.iterateRow   ,   mapPixels*(self.iterateCol+1)   ,   mapPixels*(self.iterateRow +1)  , outline="red", fill="red")
            elif map[self.iterateRow*numberOfCol+self.iterateCol]== '1':
                self.rect = self.canvas.create_rectangle(mapPixels*self.iterateCol   ,mapPixels*self.iterateRow   ,   mapPixels*(self.iterateCol+1)   ,   mapPixels*(self.iterateRow +1)  , outline="black", fill="white")
                #print('111111111111111111111111111111111111111')
            else:
                #print('0')
                self.rect = self.canvas.create_rectangle(mapPixels*self.iterateCol   ,mapPixels*self.iterateRow   ,   mapPixels*(self.iterateCol+1)   ,   mapPixels*(self.iterateRow +1)  , outline="black", fill="black")

            self.iterateCol +=1
            
            if (self.iterateRow+1)*(self.iterateCol) == numberOfElements:
                '''
                If map complete we exit
                '''
                exitFlag = 1
            elif self.iterateCol == numberOfCol:
                '''
                otherwise if the end of a row has been reached we move to the next row
                '''
                self.iterateRow +=1 
                self.iterateCol = 0
            
        
        return   
        
        
        
        
        
#********************************************************************************************************************************************************************************
#                                                Test code
#********************************************************************************************************************************************************************************

if __name__ == '__main__':        
    #don't Change or it will messup current validation based on array size
    mapHeight = 30       # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  30       # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .302*.5 # .302#Test with .5 #meters Even fraction Note: see previous note 
    
    #Test scanMain123 array********************************************************
    class scan():
        print('scanMain123 Object created')
        
    #Dictionary for lookup of location
    class position():
        pass
        
        
    position.pos = {'x': 4, 'y':5}
    
    ''' use if you need to check orgin location
    scanMain123.posX=array.array('f',[10,10,10,10,10,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0])
    scanMain123.posY=array.array('f',[9,8,7,6,5,4,3,2,1,0,-1,9,8,7,6,5,4,3,2,1,0,-1])    
    scanMain123.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scanMain123.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
    '''
    scanMain123 = scan()
    
    scanMain123.posX=array.array('f',[1,2,1,5,5.5,-4.5,-5,0,0,0,0,1,0,-1,0,.5,0,-.5,0,10,-9.6])
    scanMain123.posY=array.array('f',[1,1,2,0,0,0,0,0,5,5.5,-4.5,-5,0,1,0,-1,0,.5,0,-.5,10,-9.6])    
    scanMain123.headingPlusServoAngle=array.array('f',[-33,-33,-33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scanMain123.distance=array.array('f',[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
    

    changeMap = 0
    if changeMap == 1:
        mapHeight = 10        # 10#30      #5        # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
        mapWidth =  10        #10 #30      #5        # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
        resolution = .302*.5  #.305*.5     #.305*.5 # .305*.5 #.302#Test with .5 #meters Even fraction Note: see previous note 
        
        X = 31*resolution  # 31*resolution#14*resolution
        Y =-12*resolution  #-12*resolution #resolution*-7
        
        position.pos = {'x': X, 'y':Y} 
        
        scanMain123.posX=array.array('f',[x*resolution for x in [6,7,10,10,10,10,0,1,12,-10, -10,-11,-12,-10,-10,11,12,13,5,0,0,-10,32,22,30,20,28,26,24,18,16,14,12,10,28,31,26,29,28,0,0,-2,-4,-12,-12,-14,-14,-30,-28,-26,-24,-24,-24,-24,-30,-28,-26,-24,-24,-24,-24,9,7,3,3,10,10,10,9,15,16,17,18,0,-2,-3,-2,0,10,12,14,16]])
        scanMain123.posY=array.array('f',[y*resolution for y in [3,3,10,11,12,10,0,1,0,0,-6,-6,-6,-9,-11,-9,-9,-9,-3,-8,-7,3,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-5,-3,10,12,14,16,18,-3,31,29,31,31,29,31,29,0,0,0,0,2,4,6,-6,-6,-6,-6,-8,-10,-12,1,-3,-3,2,9,7,5,4,30,30,30,30,-30,-29,-27,-25,-24,-31,-29,-27,-25]])    
        scanMain123.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
        scanMain123.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
    
    else:
        scanMain123.posX=array.array('f',[1,2,1,5,5.5,-4.5,-5,0,0,0,0,1,0,-1,0,.5,0,-.5,0,10,-9.6])
        scanMain123.posY=array.array('f',[1,1,2,0,0,0,0,0,5,5.5,-4.5,-5,0,1,0,-1,0,.5,0,-.5,10,-9.6])    
        scanMain123.headingPlusServoAngle=array.array('f',[-33,-33,-33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
        scanMain123.distance=array.array('f',[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.
        X = 13*resolution  # 31*resolution#14*resolution
        Y =9*resolution  #-12*resolution #resolution*-7
        
        position.pos = {'x': X, 'y':Y}
        

    
    
    
    #create test map
    mapMain123 = mapObj(mapHeight, mapWidth, resolution) 
    #Test run mapTask()
    mapMain123.mapTask(scanMain123)
    #Print Map 
    
    #mapMain123.printMap(position.pos)
    
    #***********************************************************
    # Test SaveMap commented so it does not spam current directory******************
    #*****************************************************
    mapMain123.saveMap(0)
    
    
    
    #Testing readPoint    
    print('Testing readPoint')    
    a = mapMain123.readPointXY(0,5)
    print('(0,5) bit:',a,'\n')    
    a = mapMain123.readPointXY(5,0)
    print('(5,0) bit:',a,'\n')    
    a= mapMain123.readPointXY(0,0)
    print('(0,0) bit:',a,'\n')    
    a= mapMain123.readPointXY(0,5.5)
    print('(0,5.5) bit:',a)
    #fancy Map test type = 0
    #mapMain123.printMapFancy(position.pos,1)
    #mapMain123.printMapGUI(position.pos)
    mapMain123.printSavedMap()
    
    
    
    import sys
    # print('mapMain123',sys.getsizeof(mapMain123))
    # print('mapMain123.map',sys.getsizeof(mapMain123.map))
    # print('mapMain123.writeMap',sys.getsizeof(mapMain123.writeMap))
