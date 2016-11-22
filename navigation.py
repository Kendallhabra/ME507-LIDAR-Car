#ZacharyArnott
#File*************************************************************************

# Navigation Task and Functions

'''
Navigation
This task and associated functions are designed to determine a waypoint from current robot position and map 
'''

import mapping
import math

class navObj():
    print('navigation Object created')
    
    def __init__(self,mapHeight, mapWidth, resolution):
        '''
        On startup navigation initalizes for the map size
        '''
        self.mapHeight = mapHeight
        self.mapWidth = mapWidth
        self.resolution = resolution
        
        self.arrayLength = int(mapHeight/resolution)
        self.arrayWidth = int(mapWidth/resolution)
        self.arrayElements = self.arrayLength*self.arrayWidth
        self.middleElement = round(self.arrayElements/2+self.arrayWidth/2)
        #self.initialScanWidth = round(1.5/resolution)
        #print(self.initialScanWidth)
        self.numberRowAboveOrgin = (self.arrayElements/2)/self.arrayWidth
        self.numberRowBlowOrgin = self.numberRowAboveOrgin - 1
        self.numberColumnLeft = self.arrayWidth/2-1
        self.numberColumnRight = self.arrayWidth/2
        
    def navTask(self,dictionary):
        '''
        Map task scans map and determines the waypoint to be set.
        '''
        self.mapScan(dictionary)
        self.setWaypoint()
    
    
    def mapScan(self,dictionary):
        '''
        Looks up the surrounding points in the map and determines which ones have objects.
        '''
        print('Finding near by objects....')
        self.currentX = dictionary['positionX']
        self.currentY = dictionary['positionY']
       
        self.numberScans = 7 #If 7x7=> 21 element search around car. Assume odd so that the number in front and behind robot checked are equal in length
        '''Current nav map, with Robot:*   ***I don't plan on changing for now as far as size is conserned***
        0000000 
        0000000
        0000000
        000*000
        0000000
        0000000
        '''
        self.numberBeyondR = (self.numberScans-1)/2
        #print(self.numberBeyondR)
        self.scanIndex = self.numberBeyondR  #plus one counts center scan or directly beside robot
        currentScan = -self.numberBeyondR
        self.mapScanResults = [] 
        iObject = -self.numberBeyondR
        
        while currentScan < self.numberScans -self.numberBeyondR:
            '''
            Scans 7 by 7 area for objects

            Searches the north direction by iterating through each element in a column until an object is found in one column
            '''
            #print('self.numberRowAboveOrgin + self.currentY/self.resolution + iObject',self.numberRowAboveOrgin - self.currentY/self.resolution - iObject)
            if mapMain.readPoint(self.arrayElements - ((round(self.currentX/self.resolution)+currentScan)*-1+self.arrayWidth/2 + 1 + ((round(self.currentY/self.resolution)+iObject)+self.arrayLength/2-1)*self.arrayLength)) == 1:
                '''
                stores the X and Y coordinates of the object
                '''
                #print('\nFound an Object!!!')
                objX = round(self.currentX/self.resolution)+currentScan- self.scanIndex
                objY = round(self.currentY/self.resolution)+iObject
                #print('(X,Y): ', objX, objY)
                realitiveX = currentScan
                realitiveY = iObject
                #print('RealitiveX,RealitiveY: ', realitiveX,realitiveY)
                
                #relativeDistance = math.sqrt((iObject)**2+(currentScan- self.scanIndex)**2)
                #print('relativedistance: ',relativeDistance)
                self.mapScanResults.append([realitiveX,realitiveY])#
                if iObject == self.numberScans: #If the number of rows to be checked is complete we move to next column even when point found
                    #print('End column!!!')
                    currentScan +=1#next scan
                    iObject = -self.numberBeyondR#reset row
                else:#Move to next row
                    iObject +=1

            elif iObject == self.numberScans:#If the number of rows to be checked is complete we move to next column 
                #print('End column!!!')
                currentScan +=1#next scan
                iObject = -self.numberBeyondR
                
            else:
                iObject +=1#Move to next row
                #print('N.O.',end='')         
        #print('Finished!!!\n\n')
                
    def setWaypoint(self):
        '''
        Sets way point based on anaylsis of objects found in mapScan. First it will check if any objects are in the north, northWest,...,east, northEast quadrante. 
        If an object is found that variable is set to 1. (aka north = 1)
        
        Quadrant Examples:
        northQuadrant        northEastQuadrant *considering excluding the 1 directly above and besides robot (change was made refer to second NE example)
        0011100                 1100000  1100000
        0011100                 1110000  1110000
        0011100                 0111000  0110000
        000*000                 001*000  000*000
        0000000                 0000000  0000000
        0000000                 0000000  0000000
        0000000                 0000000  0000000
        '''
        print('Determining wayPoint...')
        
        northCheckList =        [[-1,3],[0,3],[1,3],[-1,2],[0,2],[1,2],[-1,1],[0,1],[1,1]]
        northWestCheckList =    [[-3,3],[-2,3],[-3,2],[-2,2],[-1,2],[-2,1],[-1,1]]#,[0,1],[-1,0]]
        westCheckList =         [[-3,1],[-2,1],[-1,1],[-3,0],[-2,0],[-1,0],[-3,-1],[-2,-1],[-1,-1]]
        southWestCheckList =    [[-3,-3],[-2,-3],[-3,-2],[-2,-2],[-1,-2],[-2,-1],[-1,-1]]#,[0,-1],[-1,0]]
        southCheckList =        [[-1,-3],[0,-3],[1,-3],[-1,-2],[0,-2],[1,-2],[-1,-1],[0,-1],[1,-1]]
        southEastCheckList =    [[3,-3],[2,-3],[3,-2],[2,-2],[1,-2],[2,-1],[1,-1]]#,[0,-1],[1,0]]
        eastCheckList =         [[3,1],[2,1],[1,1],[3,0],[2,0],[1,0],[3,-1],[2,-1],[1,-1]]
        northEastCheckList =    [[3,3],[2,3],[3,2],[2,2],[1,2],[2,1],[1,1]]#,[0,1],[1,0]]
        
        #*************************************************************************************************************
        #                     Coss Checking lists to determine which zones are flagged
        #*************************************************************************************************************
        
        #North Check**************************************
        
        if [i for i in northCheckList if i in self.mapScanResults] != []:#checks of checklist item is in the mapmapScanResults if nothing found then 
            north = 1
        else:
            north = 0
        #print('check',[i for i in self.mapScanResults if i in northCheckList])
        print('north:     ',north,'')
        
        #NorthWest Check**************************************
        
        if [i for i in self.mapScanResults if i in northWestCheckList] != []:
            northWest = 1
        else:
            northWest = 0
        #print('check',[i for i in self.mapScanResults if i in northWestCheckList])
        print('northWest: ',northWest,'')        
        
        #West Check**************************************
        
        if [i for i in westCheckList if i in self.mapScanResults] != []:
            west = 1
        else:
            west = 0
        #print('check',[i for i in self.mapScanResults if i in westCheckList])
        print('west:      ',west,'')        
        
        #southWest Check**************************************
        
        if [i for i in southWestCheckList if i in self.mapScanResults] != []:
            southWest = 1
        else:
            southWest = 0
        #print('check',[i for i in self.mapScanResults if i in southWestCheckList])
        print('southWest: ',southWest,'')
        
        #South Check**************************************
        
        if [i for i in southCheckList if i in self.mapScanResults] != []:
            south = 1
        else:
            south = 0
        #print('check',[i for i in self.mapScanResults if i in southCheckList])
        print('south:     ',south,'')
        
        #SouthEast Check**************************************
        
        if [i for i in southEastCheckList if i in self.mapScanResults] != []:
            southEast = 1
        else:
            southEast = 0
        #print('check',[i for i in self.mapScanResults if i in southEastCheckList])
        print('southEast: ',southEast,'')
        
        #East Check**************************************
        
        if [i for i in eastCheckList if i in self.mapScanResults] != []:
            east = 1
        else:
            east = 0
        #print('check',[i for i in self.mapScanResults if i in eastCheckList])
        print('East:      ',east,'')
        
        #northEast Check**************************************
        
        if [i for i in northEastCheckList if i in self.mapScanResults] != []:
            northEast = 1
        else:
            northEast = 0
        #print('check',[i for i in self.mapScanResults if i in northEastCheckList])
        print('northEast: ',northEast,'')
        
        
        #****************************************************************************************
        #                             Waypoint Conditions
        #****************************************************************************************
        
        #Case 0 move north
        if north == 0 and northWest == 0 and west == 0 and southWest == 0 and south == 0 and southEast == 0 and east == 0 and northEast == 0:
            wayX = self.currentX 
            wayY = self.currentY + 3
            self.waypoint = [wayX,wayY]
            print('Case 0 move north')
        
        #Case 5 move west from corner
        elif north == 1 and northEast == 1 and southEast == 1 and west == 0:
            wayX = self.currentX - 3
            wayY = self.currentY 
            self.waypoint = [wayX,wayY]
            print('Case 5 move west')
            
        #Case 6 move south
        elif west == 1 and northWest == 1 and north == 1 and south == 0:
            wayX = self.currentX 
            wayY = self.currentY - 3
            self.waypoint = [wayX,wayY]
            print('Case 6 move south')
        
        #Case 7 move east from corner
        elif west == 1 and southWest == 1 and south == 1 and east == 0:
            wayX = self.currentX + 3
            wayY = self.currentY 
            self.waypoint = [wayX,wayY]
            print('Case 7 move east')

        #Case 8 move north from corner
        elif south == 1 and southEast == 1 and east == 1 and north == 0:
            wayX = self.currentX 
            wayY = self.currentY + 3
            self.waypoint = [wayX,wayY]
            print('Case 5 move north')
        
        #Case 1 move north
        elif north == 0 and ( northEast == 1 or east == 1):
            wayX = self.currentX 
            wayY = self.currentY + 3
            self.waypoint = [wayX,wayY]
            print('Case 1 move north')        
        
        #Case 2 move west
        elif west == 0 and ( northWest == 1 or north == 1):
            wayX = self.currentX - 3
            wayY = self.currentY 
            self.waypoint = [wayX,wayY]
            print('Case 4 move west')
            
        #Case 3 move south
        elif south == 0 and ( southWest == 1 or west == 1):
            wayX = self.currentX 
            wayY = self.currentY - 3
            self.waypoint = [wayX,wayY]
            print('Case 3 move south')
        
        #case 4 move east
        elif east == 0 and ( southEast == 1 or south == 1):
            wayX = self.currentX + 3
            wayY = self.currentY 
            self.waypoint = [wayX,wayY]
            print('Case 4 move east')
         
         
#********************************************************************************************************************************************************************************
#                                                Test code
#********************************************************************************************************************************************************************************
if __name__ == '__main__':  
    '''
    Runs only if this file is main
    '''
    import mapping
    import array
    
    #don't Change or it will messup current validation based on array size
    mapHeight = 40 # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  40 # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .302 # .302#Test with .5 #meters Even fraction Note: see previous note 
        
    #Test scan array********************************************************
    class scanMain():
        print('scan Object created')
            
    #Dictionary for lookup of location
    dictionary = {'positionX': 32*resolution, 'positionY':resolution*32}  #dictionary = {'positionX': 5, 'positionY':5}  
    scanMain.posX=array.array('f',[10,10,10,10,10,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0,5,6.5,6.2,3.8,5.9,4.2,5.9,4.2,5.9,4.2,4.2])
    scanMain.posY=array.array('f',[9,8,7,6,5,4,3,2,1,0,-1,9,8,7,6,5,4,3,2,1,0,-1,8,6,5,5,4.2,4.2,3.9,3.9,6.1,6.1,5.8])    
    scanMain.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scanMain.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    

        
    #create test map
    mapMain = mapping.mapObj(mapHeight, mapWidth, resolution) 
    #Test run mapTask()
    mapMain.mapTask(scanMain)
    #Print Map 
        
    mapMain.printMapFancy(dictionary,1)   
    
    navMain = navObj(mapHeight, mapWidth, resolution)
    
    
    #navMain.mapScan(dictionary)
    #navMain.setWaypoint()
    
    navMain.navTask(dictionary)
    
