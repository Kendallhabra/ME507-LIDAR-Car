#ZacharyArnott
#File*************************************************************************

# Navigation Task and Functions

'''
Navigation
This task and associated functions are designed to determine a wayPointSteps from current robot position and map 
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
        self.lastDirection = 0 #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 
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
        
        self.explorerFlag = 0 #This initailises the explorer part of waypoint logic
        
    def navTask(self,dictionary):
        '''
        Map task scans map and determines the wayPointSteps to be set.
        '''
        self.mapScan(dictionary)
        self.setwayPointSteps()
    
    
    def mapScan(self,dictionary):
        '''
        Looks up the surrounding points in the map and determines which ones have objects.
        '''
        print('\nFinding near by objects....')
        self.currentX = round(dictionary['positionX']/self.resolution)
        self.currentY = round(dictionary['positionY']/self.resolution)
       
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
            if mapMain.readPoint(self.arrayElements - ((round(self.currentX)+currentScan)*-1+self.arrayWidth/2 + 1 + ((round(self.currentY)+iObject)+self.arrayLength/2-1)*self.arrayLength)) == 1:
                '''
                stores the X and Y coordinates of the object
                '''
                #print('\nFound an Object!!!')
                objX = round(self.currentX)+currentScan- self.scanIndex
                objY = round(self.currentY)+iObject
                #print('(X,Y): ', objX, objY)
                realitiveX = currentScan
                realitiveY = iObject
                #print('RealitiveX,RealitiveY: ', realitiveX,realitiveY)

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
                
    def setwayPointSteps(self):
        '''
        Sets way point based on anaylsis of objects found in mapScan. First it will check if any objects are in the north, northWest,...,east, northEast quadrante. 
        If an object is found that variable is set to 1. (aka north = 1)
        
        Quadrant Examples:
        northQuadrant        northEastQuadrant       northClose
        0011100                  1100000             0000000
        0011100                  1110000             0000000
        0011100                  0110000             0011100
        000*000                  000*000             000*000
        0000000                  0000000             0000000
        0000000                  0000000             0000000
        0000000                  0000000             0000000
        
        This is turned into quadrants true false logic. Based on which of these quadrants is triggered waypoint decisions are made
        
                           Example
        X X X    NW N NW   T F F
        
        X * X    W  *  E   T * F
        
        X X X    SW S SE   T T T 
        
        
        '''
        print('Determining wayPointSteps...')
        
        #Here are the checklist of points in each quadrant
        
        northCheckList =        [[-1,3],[0,3],[1,3],[-1,2],[0,2],[1,2],[-1,1],[0,1],[1,1]]
        westCheckList =         [[-3,1],[-2,1],[-1,1],[-3,0],[-2,0],[-1,0],[-3,-1],[-2,-1],[-1,-1]]
        southCheckList =        [[-1,-3],[0,-3],[1,-3],[-1,-2],[0,-2],[1,-2],[-1,-1],[0,-1],[1,-1]]
        eastCheckList =         [[3,1],[2,1],[1,1],[3,0],[2,0],[1,0],[3,-1],[2,-1],[1,-1]]
        
        northWestCheckList =    [[-3,3],[-2,3],[-3,2],[-2,2],[-1,2],[-2,1],[-1,1]]#,[0,1],[-1,0]]
        southWestCheckList =    [[-3,-3],[-2,-3],[-3,-2],[-2,-2],[-1,-2],[-2,-1],[-1,-1]]#,[0,-1],[-1,0]]
        southEastCheckList =    [[3,-3],[2,-3],[3,-2],[2,-2],[1,-2],[2,-1],[1,-1]]#,[0,-1],[1,0]]
        northEastCheckList =    [[3,3],[2,3],[3,2],[2,2],[1,2],[2,1],[1,1]]#,[0,1],[1,0]]
        
        #These check if the robot is directly by the wall and logic tries to move car to be atleast 1 element way from wall
        northCloseCheck =       [[0,1]]     #[[-1,1],[0,1],[1,1]]
        westCloseCheck =        [[-1,0]]    #[[-1,-1],[-1,0],[-1,1]]
        southCloseCheck =       [[0,-1]]    #[[-1,-1],[0,-1],[1,-1]]
        eastCloseCheck =        [[1,0]]     #[[1,-1],[1,0],[1,1]]
        
        
        #*************************************************************************************************************
        #                     Coss Checking lists to determine which zones are flagged
        #*************************************************************************************************************
        
        #North Check**************************************
        
        if [i for i in northCheckList if i in self.mapScanResults] != []:
            '''
            Checks of checklist item is in the mapmapScanResults if nothing found then it is set to false
            '''
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
        
        
        #north Close Check**************************************
        
        if [i for i in northCloseCheck if i in self.mapScanResults] != []:
            northClose = 1
        else:
            northClose = 0
        #print('check',[i for i in self.mapScanResults if i in northEastCheckList])
        print('northClose:',northClose,'')
        
        #west Close Check**************************************
        
        if [i for i in westCloseCheck if i in self.mapScanResults] != []:
            westClose = 1
        else:
            westClose = 0
        #print('check',[i for i in self.mapScanResults if i in northEastCheckList])
        print('westClose: ',westClose,'')
        
        #south Close Check**************************************
        
        if [i for i in southCloseCheck if i in self.mapScanResults] != []:
            southClose = 1
        else:
            southClose = 0
        #print('check',[i for i in self.mapScanResults if i in northEastCheckList])
        print('southClose:',southClose,'')
        
        #east Close Check**************************************
        
        if [i for i in eastCloseCheck if i in self.mapScanResults] != []:
            eastClose = 1
        else:
            eastClose = 0
        #print('check',[i for i in self.mapScanResults if i in northEastCheckList])
        print('eastClose: ',eastClose,'')
        
        
        #****************************************************************************************
        #                             wayPointSteps Conditions
        #****************************************************************************************
        
        
        
        
        #This can be customised depending on how often explore needs to be triggered
        explorerEvents = 0 #Turns on cycle based expoler
        stopExplorer = 1 #Turns on cycle based exit expoler if you do not want expoler to exit on its own
        if explorerEvents == 1:
            ''' This event/cycle based control of explorer. It may not be needed.
            '''
            try:
                self.expolerCounter +=1
                print('self.expolerCounter +=1',self.expolerCounter)
            except AttributeError:
                self.expolerCounter = 0
                #self.explorerFlag = 0 in init
        
            if self.expolerCounter == 7:#number of counts till explorer is triggered
                self.explorerFlag = 1
            elif self.expolerCounter == 10 and stopExplorer == 1:#number of steps till expolered turned off
                 self.explorerFlag = 0
                 self.expolerCounter = 0
        
        
        #*************************
        self.wayPointdistance = 2 # a number between 1 and 3 insure its in the scanned region
        #*************************
        
        

        #currently explore is inactive its goal is to prevent the orbiting of a chair or table
        if self.explorerFlag == 1:
            print('EXPLORE')
            '''
            The explore cases conitnue in the same direction as the last movement so long as it is clear to do so. If it is not clear explore is turned off.
            '''
            
            #Case 12 move north last move north
            if north == 0 and self.lastDirection == 1 : #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 
                '''
                Only to current direction is checked to be clear. Then waypoint is set.
                '''
                wayX = self.currentX 
                wayY = self.currentY + self.wayPointdistance
                self.wayPointSteps = [wayX,wayY]
                print('Case 12 move north')
                
            #Case 13 move west last move west
            elif west == 0 and self.lastDirection == 2 :
                wayX = self.currentX - self.wayPointdistance
                wayY = self.currentY 
                self.wayPointSteps = [wayX,wayY]
                print('Case 13 move west')
                
            #Case 14 move north last move north
            elif south == 0 and self.lastDirection == 3 :
                wayX = self.currentX 
                wayY = self.currentY - self.wayPointdistance
                self.wayPointSteps = [wayX,wayY]
                print('Case 14 move south')
            
            #Case 15 move east last move east
            elif east == 0 and self.lastDirection == 4 :
                wayX = self.currentX + self.wayPointdistance
                wayY = self.currentY 
                self.wayPointSteps = [wayX,wayY]
                print('Case 15 move east')
            else: #Turns off explore if no move possible in same direction and the normal cases are tried
                self.explorerFlag = 0
                self.expolerCounter = 0
                print('EXIT EXPLORE!')
            
                
        elif self.explorerFlag == 0: #*********************************************************************************************************************************************
            '''
            These are the standard logic arguments for waypoint setting.
            '''
            #Case 0 move north
            twoStepsBack = self.lastDirection #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 
            if north == 0 and northWest == 0 and west == 0 and southWest == 0 and south == 0 and southEast == 0 and east == 0 and northEast == 0:
                ''' W
                   FFF
                   F*F
                   FFF'''
                wayX = self.currentX 
                wayY = self.currentY + self.wayPointdistance
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 1 #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 
                print('Case 0 move north')
            
            #Case 5 move west from corner
            elif north == 1 and northEast == 1 and southEast == 1 and west == 0: #may be better to change north to north west, but its not broken of mi no going to fix it.
                ''' 
                     TT
                   WF* 
                      T'''
                wayX = self.currentX - self.wayPointdistance
                wayY = self.currentY 
                if northClose ==  1:
                    wayY = self.currentY -1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 2
                print('Case 5 move west')
                
            #Case 6 move south from corner
            elif west == 1 and northWest == 1 and north == 1 and south == 0:
                wayX = self.currentX 
                wayY = self.currentY - self.wayPointdistance
                if westClose == 1:
                    wayX = self.currentX + 1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 3
                print('Case 6 move south')
            
            #Case 7 move east from corner
            elif west == 1 and southWest == 1 and south == 1 and east == 0:
                wayX = self.currentX + self.wayPointdistance
                wayY = self.currentY 
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 4
                if southClose == 1:
                    wayY = self.currentY + 1
                    print('close')
                print('Case 7 move east')

            #Case 8 move north from corner
            elif south == 1 and southEast == 1 and east == 1 and north == 0:
                wayX = self.currentX 
                wayY = self.currentY + self.wayPointdistance
                if eastClose == 1:
                    wayX = self.currentX - 1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 1
                print('Case 8 move north')
            
            #Case 1 move north
            elif north == 0 and ( northEast == 1 or east == 1 )and west == 0: #and northWest ==0 and southWest == 0
                ''' W
                    FT
                   F*T
                   '''
                wayX = self.currentX 
                wayY = self.currentY + self.wayPointdistance
                if eastClose == 1:
                    wayX = self.currentX - 1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 1
                print('Case 1 move north')        
            
            #Case 2 move west
            elif west == 0 and ( northWest == 1 or north == 1 )and south ==  0 : #and southEast == 0 and southWest ==0 #or northEast == 1
                wayX = self.currentX - self.wayPointdistance
                wayY = self.currentY 
                if northClose ==  1:
                    wayY = self.currentY -1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 2
                print('Case 4 move west')
                
            #Case 3 move south
            elif south == 0 and ( southWest == 1 or west == 1 ) and east == 0 : #and northEast == 0 and southEast == 0#or northWest == 1
                wayX = self.currentX 
                wayY = self.currentY - self.wayPointdistance
                if westClose == 1:
                    wayX = self.currentX + 1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 3
                print('Case 3 move south')
            
            #case 4 move east
            elif east == 0 and ( southEast == 1 or south == 1 ) and north == 0 : #and northEast == 0 and northWest == 0#or southWest == 1
                wayX = self.currentX + self.wayPointdistance
                wayY = self.currentY 
                if southClose == 1:
                    wayY = self.currentY + 1
                    print('close')
                self.wayPointSteps = [wayX,wayY]
                self.lastDirection = 4
                print('Case 4 move east')
            
            if (twoStepsBack == 2 and self.lastDirection == 4) or (twoStepsBack == 4 and self.lastDirection == 2) or (twoStepsBack == 1 and self.lastDirection == 3) or (twoStepsBack == 3 and self.lastDirection == 1):
                self.explorerFlag = 1
                print('last move backtrack=> explorer')
            
            
            #************************
            #These case work based on the previous direction of travel. To deal with doors and so on.
            #************************
            #case 9 north/south door*****************
            elif (west == 1 ) and (east == 1 ): #or southWest == 1 or northWest == 1  #or southEast == 1 or northEast == 1
                '''  W
                    T*T
                      '''
                if self.lastDirection == 1:
                    wayX = self.currentX 
                    wayY = self.currentY + self.wayPointdistance
                    self.wayPointSteps = [wayX,wayY]
                    print('Case 9 move north')
                    
                else:
                    self.lastDirection = 3
                    wayX = self.currentX 
                    wayY = self.currentY - self.wayPointdistance
                    self.wayPointSteps = [wayX,wayY]
                    print('Case 9 move south')
            
            
            #case 10 east/west door*****************
            elif (north == 1 ) and (south == 1):#or northWest ==1 or northEast == 1 # or southEast == 1 or southWest == 1 #added lastDirection arrugment 1,2,3,4 (N,W,S,E) then remove door stuff replace by last direction
                '''  T
                     *W
                     T'''
                if self.lastDirection == 4:
                    wayX = self.currentX + self.wayPointdistance
                    wayY = self.currentY 
                    self.wayPointSteps = [wayX,wayY]
                    print('Case 10 move east')
                    
                else:
                    self.lastDirection = 2
                    wayX = self.currentX - self.wayPointdistance
                    wayY = self.currentY 
                    self.wayPointSteps = [wayX,wayY]
                    print('Case 10 move west')
                
                
                        
        self.wayPoint = [self.wayPointSteps[0]*self.resolution,self.wayPointSteps[1]*self.resolution] #converts waypoint in map steps to meters
         
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
    mapHeight = 10 # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  10 # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .305 # .302#Test with .5 #meters Even fraction Note: see previous note 
        
    #Test scan array********************************************************
    class scanMain():
        print('scan Object created')
            
    #Dictionary for lookup of location
    dictionary = {'positionX': 14*resolution, 'positionY':resolution*-8}  #dictionary = {'positionX': 5, 'positionY':5}  
    #scanMain.posX=array.array('f',[10,10,10,10,10,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0,5,6.5,6.2,3.8,5.9,4.2,5.9,4.2,5.9,4.2,4.2,0,1])
    #scanMain.posY=array.array('f',[9,8,7,6,5,4,3,2,1,0,-1,9,8,7,6,5,4,3,2,1,0,-1,8,6,5,5,4.2,4.2,3.9,3.9,6.1,6.1,5.8,0,1])    
    #scanMain.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    #scanMain.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
    
    scanMain.posX=array.array('f',[x*resolution for x in [6,7,10,10,10,10,0,1]])
    scanMain.posY=array.array('f',[x*resolution for x in [3,3,10,11,12,10,0,1]])    
    scanMain.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
    scanMain.distance=array.array('f',[0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
    
    
        
    #create test map
    mapMain = mapping.mapObj(mapHeight, mapWidth, resolution) 
    #Test run mapTask()
    mapMain.mapTask(scanMain)
    #Print Map 
        
    mapMain.printMapFancy(dictionary,1)   
    
    navMain = navObj(mapHeight, mapWidth, resolution)
    
    
    #navMain.mapScan(dictionary)
    #navMain.setwayPointSteps()
    
    
    navMain.navTask(dictionary)
    print('\nRobot location')
    print('[',navMain.currentX,',',navMain.currentY,']','(steps)')
    print('[',dictionary['positionX'],dictionary['positionY'],']')
    print('Waypoint')
    print(navMain.wayPointSteps,'(steps)')
    print(navMain.wayPoint,'(meters)')
    
    
    
    #*************************************************************************************************
    #  Test navigation assumes Robot only makes it 2 feet from its current waypoint before its updated
    #*************************************************************************************************
    
    #**************
    #Set Prompt height to 3000!!!!!!!!
    #**************
    
    
    
    crazy = 0 # did to set promp height to atleast 5000???
    
    if crazy == 1: 
        
        scanMain.posX=array.array('f',[x*resolution for x in [6,7,10,10,10,10,0,1,12,-10, -10,-11,-12,-10,-10,11,12,13,5]])
        scanMain.posY=array.array('f',[y*resolution for y in [3,3,10,11,12,10,0,1,0,0,-6,-6,-6,-9,-11,-9,-9,-9,-3]])    
        scanMain.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
        scanMain.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
        mapMain.writemap(scanMain)
        counter = 0
        
        while counter < 100:
            print('\nIteration', counter, '***************************************************')
            mapMain.printMapFancy(dictionary,1,0)
            navMain.navTask(dictionary)
            dictionary = {'positionX': navMain.wayPoint[0], 'positionY':navMain.wayPoint[1]}
            counter +=1
        
