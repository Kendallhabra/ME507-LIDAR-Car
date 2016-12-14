#Zachary Arnott
#mapping printer
'''package docstring
This prints the map to command prompt this is done for testing and is in a seperate module to save memory on pyboard
since we do not need this on the pyboard. navigation test code calls the fancy version of print map.
'''
import mapping
import array
import os 
 

class printObj(object):
    '''INCLUDE = config_file_name
    Creates and adds anylzed sensor data to the map data. It stores in in the class as mapping.map and can read the map with readPoint()
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
        mapping.mapHeight = self.arrayLength*resolution
        mapping.mapWidth = self.arrayWidth*resolution
        self.resolution = resolution
        #defines the byte array
        os.system("mode con cols=100 lines=73")
        self.numberRowAboveOrgin = (self.arrayElements/2)/self.arrayWidth
        self.numberRowBlowOrgin = self.numberRowAboveOrgin - 1
        self.numberColumnLeft = self.arrayWidth/2-1
        self.numberColumnRight = self.arrayWidth/2
        


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
                print(mapping.map[self.iterateRow*self.arrayLength+self.iterateCol], end="")#printing a single bit
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
            #print('*',end="")
            iter +=1
        #print(end='\n')
        
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            if self.arrayElements - (round(dictionary['x']/self.resolution)*-1+self.arrayWidth/2 + 1 + (round(dictionary['y']/self.resolution)+self.arrayLength/2-1)*self.arrayLength) == self.iterateRow*self.arrayLength+self.iterateCol:
                print(self.robot, end="")
            elif mapping.map[self.iterateRow*self.arrayLength+self.iterateCol] == 1:
                print(self.emptyType, end="")#printing a single bit

            else:
                print(self.fillType,end="")
            self.iterateCol +=1
            
            if (self.iterateRow+1)*(self.iterateCol) == self.arrayElements:#If map complete we exit
                exitFlag = 1
            elif self.iterateCol == self.arrayWidth:#otherwise if the end of a row has been reached we move to the next row
                self.iterateRow +=1 
                self.iterateCol = 0
                print(end="\n")#print(end="*\n")
                
        iter = 0
        #print(end='*\n')
        while iter < self.arrayWidth:
            #print('*',end="")
            iter +=1
        print(end='\n')
        return      
