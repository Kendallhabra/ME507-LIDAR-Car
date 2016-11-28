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
    #print('Navigation Object created')
    
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
        ##print(self.initialScanWidth)
        self.numberRowAboveOrgin = (self.arrayElements/2)/self.arrayWidth
        self.numberRowBlowOrgin = self.numberRowAboveOrgin - 1
        self.numberColumnLeft = self.arrayWidth/2-1
        self.numberColumnRight = self.arrayWidth/2
        
        self.explorerFlag = 0 #This initailises the explorer part of waypoint logic
        
        
        self.explorerCounter = 1
        
        #*************************
        self.wayPointdistance = 3 #[3 for operation!!! 1 for simulation ] a number between 1 and 3 insure its in the scanned region
        #*************************
        
        '''
        Here I initialzes all of the checks and past robot position so that navigation knows when to update waypoint.
        The waypoint will only be updated if the checks change or the robot reaches the next quadrant(aka move one resolution distance).
        '''
        
        #initializing navigation history
        self.wayPointSteps = [0,0] #keeps record of location of current waypoint set point.
        self.lastPosition = ['null'] #Assume we start in the middle of the map [0,0]
        
        self.north = 2
        self.northWest = 2
        self.west = 2
        self.southWest = 2
        self.south = 2
        self.east = 2
        self.northEast = 2
        self.northClose = 2
        self.westClose = 2
        self.southClose = 2
        self.eastClose = 2
        self.explorerNorth = 2
        self.explorerWest = 2
        self.explorerSouth = 2
        self.explorerEast = 2
        self.nothingHappened = 0 #ensure the robot does not stop if new waypoint is not set for some reason. It ensure logic runs on next cycle
        
    def navTask(self,dictionary):
        '''
        Map task scans map and determines the wayPointSteps to be set.
        '''
        self.scanMap(dictionary)
        self.setWayPoint()
    
    def scanMap(self,dictionary):
        '''
        Looks up the surrounding points in the map and determines which ones have objects.
        '''
        ##print('\nFinding near by objects....')
        self.currentX = round(dictionary['positionX']/self.resolution)
        self.currentY = round(dictionary['positionY']/self.resolution)
        
        self.numberScans = 7 # This is a 7x7=> 21 element search around robot. 
        '''Current nav map, with Robot:*  
        0000000 
        0000000
        0000000
        000*000
        0000000
        0000000
        '''
        self.numberBeyondR = (self.numberScans-1)/2
        ##print(self.numberBeyondR)
        self.scanIndex = self.numberBeyondR  #plus one counts center scan or directly beside robot
        currentScan = -self.numberBeyondR
        self.scanMapResults = [] 
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
                ##print('\nFound an Object!!!')
                objX = round(self.currentX)+currentScan- self.scanIndex
                objY = round(self.currentY)+iObject
                ##print('(X,Y): ', objX, objY)
                realitiveX = currentScan
                realitiveY = iObject
                ##print('RealitiveX,RealitiveY: ', realitiveX,realitiveY)

                self.scanMapResults.append([realitiveX,realitiveY])#
                if iObject == self.numberScans: #If the number of rows to be checked is complete we move to next column even when point found
                    ##print('End column!!!')
                    currentScan +=1#next scan
                    iObject = -self.numberBeyondR#reset row
                else:#Move to next row
                    iObject +=1

            elif iObject == self.numberScans:#If the number of rows to be checked is complete we move to next column 
                ##print('End column!!!')
                currentScan +=1#next scan
                iObject = -self.numberBeyondR
                
            else:
                iObject +=1#Move to next row
                ##print('N.O.',end='')         
        ##print('Finished!!!\n\n')
                
    def setWayPoint(self):
        '''
        Sets way point based on anaylsis of objects found in scanMap. First it will check if any objects are in the north, northWest,...,east, northEast quadrante. 
        If an object is found that variable is set to 1. (aka north = 1) The robot runs around the room counter clockwise. I could have set it up clockwise, but this 
        was just how I envisioned it at the time. The assumption of CCW is what ensure the robot visits the entire room systematically in a relitive circle. I have used 
        two sets of logicals normal and explorer. I use explorer to prevent the robot from getting caught in infinate loops of forward backwards for example. Explorer only 
        Looks at the direction it intends to move in. While the normal logic looks at all of the quadrants around the robot. I am currently storing the last travel direction
        of the robot as (1,2,3,4) => (N,W,S,E). This ensure I don't get stuck in an infinit loop near a table of tight space.
        
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
        ##print('Determining wayPointSteps...')
        #*************Here are the checklist of points in each quadrant******************************************************************************
        northCheckList =        [[-1,3],[0,3],[1,3],[-1,2],[0,2],[1,2],[-1,1],[0,1],[1,1]]
        westCheckList =         [[-3,1],[-2,1],[-1,1],[-3,0],[-2,0],[-1,0],[-3,-1],[-2,-1],[-1,-1]]
        southCheckList =        [[-1,-3],[0,-3],[1,-3],[-1,-2],[0,-2],[1,-2],[-1,-1],[0,-1],[1,-1]]
        eastCheckList =         [[3,1],[2,1],[1,1],[3,0],[2,0],[1,0],[3,-1],[2,-1],[1,-1]]
        
        explorerNorthCheckList =        [          [2,0],[2,1],[2,1]]        #,[-2,0],[-2,1],[-2,2]
        explorerWestCheckList =         [        [0,2],[-1,2],[-2,2]]        #,[0,-2],[-1,-2],[-2,-2]
        explorerSouthCheckList =        [     [-2,0],[-2,-1],[-2,-2]]        #,[2,0],[2,-1],[2,-2]
        explorerEastCheckList =         [       [0,-2],[1,-2],[2,-2]]        #[0,2],[1,2],[2,2],
        
        northWestCheckList =    [[-3,3],[-2,3],[-3,2],[-2,2],[-1,2],[-2,1],[-1,1]]#,[0,1],[-1,0]]
        southWestCheckList =    [[-3,-3],[-2,-3],[-3,-2],[-2,-2],[-1,-2],[-2,-1],[-1,-1]]#,[0,-1],[-1,0]]
        southEastCheckList =    [[3,-3],[2,-3],[3,-2],[2,-2],[1,-2],[2,-1],[1,-1]]#,[0,-1],[1,0]]
        northEastCheckList =    [[3,3],[2,3],[3,2],[2,2],[1,2],[2,1],[1,1]]#,[0,1],[1,0]]
        
        #These check if the robot is directly by the wall and logic tries to move robot to be atleast 1 element way from wall
        northCloseCheck =       [[0,1]]     #[[-1,1],[0,1],[1,1]]
        westCloseCheck =        [[-1,0]]    #[[-1,-1],[-1,0],[-1,1]]
        southCloseCheck =       [[0,-1]]    #[[-1,-1],[0,-1],[1,-1]]
        eastCloseCheck =        [[1,0]]     #[[1,-1],[1,0],[1,1]]
        #*************************************************************************************************************
        #                     Coss Checking lists to determine which zones are flagged
        #*************************************************************************************************************
        
        #North Check**************************************
        if [i for i in northCheckList if i in self.scanMapResults] != []:
            '''
            Checks of checklist item is in the mapscanMapResults if nothing found then it is set to false
            '''
            self.north = 1
        else:
            self.north = 0
        ##print('check',[i for i in self.scanMapResults if i in northCheckList])
        #print('north:     ',self.north,'')
        
        #NorthWest Check**************************************
        if [i for i in self.scanMapResults if i in northWestCheckList] != []:
            self.northWest = 1
        else:
            self.northWest = 0
        ##print('check',[i for i in self.scanMapResults if i in northWestCheckList])
        #print('northWest: ',self.northWest,'')        
        
        #West Check**************************************
        if [i for i in westCheckList if i in self.scanMapResults] != []:
            self.west = 1
        else:
            self.west = 0
        ##print('check',[i for i in self.scanMapResults if i in westCheckList])
        #print('west:      ',self.west,'')        
        
        #southWest Check**************************************
        if [i for i in southWestCheckList if i in self.scanMapResults] != []:
            self.southWest = 1
        else:
            self.southWest = 0
        ##print('check',[i for i in self.scanMapResults if i in southWestCheckList])
        #print('southWest: ',self.southWest,'')
        
        #South Check**************************************
        if [i for i in southCheckList if i in self.scanMapResults] != []:
            self.south = 1
        else:
            self.south = 0
        ##print('check',[i for i in self.scanMapResults if i in southCheckList])
        #print('south:     ',self.south,'')
        
        #SouthEast Check************************************** 
        if [i for i in southEastCheckList if i in self.scanMapResults] != []:
            self.southEast = 1
        else:
            self.southEast = 0
        ##print('check',[i for i in self.scanMapResults if i in southEastCheckList])
        #print('southEast: ',self.southEast,'')
        
        #East Check**************************************
        if [i for i in eastCheckList if i in self.scanMapResults] != []:
            self.east = 1
        else:
            self.east = 0
        ##print('check',[i for i in self.scanMapResults if i in eastCheckList])
        #print('East:      ',self.east,'')
        
        #northEast Check**************************************
        if [i for i in northEastCheckList if i in self.scanMapResults] != []:
            self.northEast = 1
        else:
            self.northEast = 0
        ##print('check',[i for i in self.scanMapResults if i in northEastCheckList])
        #print('northEast: ',self.northEast,'')
        
        
        #north Close Check**************************************
        if [i for i in northCloseCheck if i in self.scanMapResults] != []:
            self.northClose = 1
        else:
            self.northClose = 0
        ##print('check',[i for i in self.scanMapResults if i in northEastCheckList])
        #print('northClose:',self.northClose,'')
        
        #west Close Check**************************************
        if [i for i in westCloseCheck if i in self.scanMapResults] != []:
            self.westClose = 1
        else:
            self.westClose = 0
        ##print('check',[i for i in self.scanMapResults if i in northEastCheckList])
        #print('westClose: ',self.westClose,'')
        
        #south Close Check**************************************
        
        if [i for i in southCloseCheck if i in self.scanMapResults] != []:
            self.southClose = 1
        else:
            self.southClose = 0
        ##print('check',[i for i in self.scanMapResults if i in northEastCheckList])
        #print('southClose:',self.southClose,'')

        #east Close Check**************************************
        if [i for i in eastCloseCheck if i in self.scanMapResults] != []:
            self.eastClose = 1
        else:
            self.eastClose = 0
        ##print('check',[i for i in self.scanMapResults if i in northEastCheckList])
        #print('eastClose: ',self.eastClose,'')
        
        #Explorer checks
        
        #ExplorerNorth*****************************************
        if [i for i in explorerNorthCheckList if i in self.scanMapResults] != []:
            self.explorerNorth = 1
        else:
            self.explorerNorth = 0
        ##print('check',[i for i in self.scanMapResults if i in explorerNorthCheckList])
        #print('explorerNorth: ',self.explorerNorth,'')
        
        #ExplorerWest*****************************************
        if [i for i in explorerWestCheckList if i in self.scanMapResults] != []:
            self.explorerWest = 1
        else:
            self.explorerWest = 0
        ##print('check',[i for i in self.scanMapResults if i in explorerWestCheckList])
        #print('explorerWest: ',self.explorerWest,'')
        
        #ExplorerSouth*****************************************
        if [i for i in explorerSouthCheckList if i in self.scanMapResults] != []:
            self.explorerSouth = 1
        else:
            self.explorerSouth = 0
        ##print('check',[i for i in self.scanMapResults if i in explorerSouthCheckList])
        #print('explorerSouth: ',self.explorerSouth,'')
        
        #ExplorerEast*****************************************
        if [i for i in explorerEastCheckList if i in self.scanMapResults] != []:
            self.explorerEast = 1
        else:
            self.explorerEast = 0
        ##print('check',[i for i in self.scanMapResults if i in explorerEastCheckList])
        #print('explorerEast: ',self.explorerEast,'')
        #****************************************************************************************
        #                             wayPointSteps Conditions
        #****************************************************************************************
        '''
        This can be customised depending on how often explore needs to be triggered currently it is only triggered if the robot backtracks 
        which would happen in a tight space where the robot would have to go in reverse or turn around in place. 
        '''
        
        self.explorerCounter +=1
        
        
               
        if self.explorerCounter == -1:
            '''
            number of counts till explorer is triggered -1 mean we dont want it triggered ensure that you put a limiter on it if you dont want it running till the next object is found
            '''  
            self.explorerFlag = 1    

        if (self.lastPosition != [self.currentX,self.currentY] or self.lastNorth != self.north or self.lastNorthWest != self.northWest or self.lastWest != self.west or 
            self.lastSouthWest != self.southWest or self.lastSouth != self.south or self.lastEast != self.east or self.lastNorthEast != self.northEast or 
            self.lastNorthClose != self.northClose or self.lastWestClose != self.westClose or self.lastSouthClose != self.southClose or self.lastEastClose != self.eastClose or 
            self.lastExplorerNorth != self.explorerNorth or self.lastExplorerWest != self.explorerWest or self.lastExplorerSouth != self.explorerSouth or 
            self.lastExplorerEast != self.explorerEast or (self.twoStepsBack == 2 and self.lastDirection == 4) or (self.twoStepsBack == 4 and self.lastDirection == 2) or 
            (self.twoStepsBack == 1 and self.lastDirection == 3) or (self.twoStepsBack == 3 and self.lastDirection == 1) or self.nothingHappened == 1):
            '''
            This if statment prevents the waypoint from being updated unless one of the logics has changed or the robot position has change by one quadrant this ensures logic work the same
            way as it did in simulation. The logics of switching directings was included because when switching logics from normal to expoler the robot may not have moved and the logic may
            not have changed. This because as a last resort of the robot does not move under normal logics the robot switchs to explore which will get the robot moving again.
            '''
            print('update waypoint!!!!')
            #******************************************************************************************
            #                           Explorer
            #***************************************************************************************
            if self.explorerFlag == 1 or self.nothingHappened == 1:
                #print('running explorer')
                '''
                The explore cases conitnue in the same direction as the last movement so long as it is clear to do so. If it is not clear explore is turned off.
                '''
                self.nothingHappened = 0
                #Case 12 move north last move north
                if self.north == 0 and self.lastDirection == 1 : #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 
                    '''
                    Only to current direction is checked to be clear. Then waypoint is set in that direction.
                    '''
                    wayX = self.currentX
                    if self.explorerNorth == 0:
                        '''
                        The robot offsets its self if possible from the direction it entered a tight area to ensure it does not fall back into the tile space.
                        This would include the robot driving under a table without the offset the robot would backup and the drive straight back under the table.
                        '''
                        wayX = wayX + 1
                    wayY = self.currentY + self.wayPointdistance
                    self.wayPointSteps = [wayX,wayY]
                    #print('Case 12 move north')
                    
                #Case 13 move west last move west
                elif self.west == 0 and self.lastDirection == 2 :
                    wayX = self.currentX - self.wayPointdistance
                    wayY = self.currentY
                    if self.explorerWest == 0:
                        wayY = wayY + 1
                    self.wayPointSteps = [wayX,wayY]
                    #print('Case 13 move west')
                    
                #Case 14 move north last move north
                elif self.south == 0 and self.lastDirection == 3 :
                    wayX = self.currentX 
                    if self.explorerSouth == 0:
                        wayX = wayX - 1
                    wayY = self.currentY - self.wayPointdistance
                    self.wayPointSteps = [wayX,wayY]
                    #print('Case 14 move south')
                
                #Case 15 move east last move east
                elif self.east == 0 and self.lastDirection == 4 :
                    wayX = self.currentX + self.wayPointdistance
                    wayY = self.currentY 
                    if self.explorerEast == 0:
                        wayY = wayY - 1
                    self.wayPointSteps = [wayX,wayY]
                    #print('Case 15 move east')
                    
                #case 16 move north*************************************************************************************************
                elif self.north == 0:
                    wayX = self.currentX 
                    wayY = self.currentY + self.wayPointdistance
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 1
                    #print('Case 16 move north')
                
                #case 17 move south
                elif self.south == 0:
                    wayX = self.currentX 
                    wayY = self.currentY - self.wayPointdistance
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 3
                    #print('Case 17 move south')
                    
                #case 18 move west
                elif self.west == 0:
                    wayX = self.currentX - self.wayPointdistance
                    wayY = self.currentY 
                    self.lastDirection = 2
                    self.wayPointSteps = [wayX,wayY]
                    #print('Case 18 move west')
                    
                #case 19 move east
                elif self.east == 0:
                    wayX = self.currentX + self.wayPointdistance
                    wayY = self.currentY 
                    self.lastDirection = 4
                    self.wayPointSteps = [wayX,wayY]
                    #print('Case 19 move east')
                    
                else: #Turns off explore if no move possible in same direction and the normal cases are tried
                    self.explorerFlag = 0
                    self.explorerCounter = 0
                #**********turn of explorer control*******************    
                if (self.explorerCounter == 4 ) :#or (self.explorerCounter == 22) #number of steps till expolered turned off
                    '''
                    If the explorer counter is on it stops it and changes to normal logic
                    '''
                    self.explorerFlag = 0
                    self.explorerCounter = 0
                    if self.lastDirection == 1:
                        self.lastDirection = 5 #provides 0Case info about last explorer direction (1,2,3,4) => (N,W,S,E) => (5,6,7,8)
                    elif self.lastDirection == 2:
                        self.lastDirection = 6
                    elif self.lastDirection == 3:
                        self.lastDirection = 7
                    elif self.lastDirection == 4:
                        self.lastDirection = 8
                    ##print('EXIT EXPLORE!')
                
                
            #***************************************************************************************************************   
            #                                       Normal Logic
            #***************************************************************************************************************
            elif self.explorerFlag == 0 or self.nothingHappened == 1: 
                self.nothingHappened = 0
                '''
                These are the standard logic arguments for waypoint setting.
                '''
                self.twoStepsBack = self.lastDirection #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 
                #twoStepsback lets me draw a comparison if direction between the previous to steps to prevent getting stuck in a forward back infinate loop
                #print('running normal')
                #Case 0 after explorer
                if self.north == 0 and self.northWest == 0 and self.west == 0 and self.southWest == 0 and self.south == 0 and self.southEast == 0 and self.east == 0 and self.northEast == 0:
                    ''' W      This is an example of the scanned logic and required quardrant responses. T is object full, F is no object, W is waypoint direction. 
                       FFF
                       F*F
                       FFF'''
                    if self.lastDirection == 5:    #(1,2,3,4) => (N,W,S,E) => (5,6,7,8)
                        wayX = self.currentX + self.wayPointdistance
                        wayY = self.currentY - self.wayPointdistance
                        #print('Case 0 after Explorer move southEast')
                    elif self.lastDirection == 6:
                        wayX = self.currentX + self.wayPointdistance
                        wayY = self.currentY + self.wayPointdistance
                        #print('Case 0 after Explorer move northEast')
                    elif self.lastDirection == 7:
                        wayX = self.currentX - self.wayPointdistance
                        wayY = self.currentY + self.wayPointdistance
                        #print('Case 0 after Explorer move northWest')
                    elif self.lastDirection == 8: 
                        wayX = self.currentX - self.wayPointdistance
                        wayY = self.currentY - self.wayPointdistance
                        #print('Case 0 after Explorer move southWest')
                    else:                                               #if explorer was not the last logic move north
                        wayX = self.currentX 
                        wayY = self.currentY + self.wayPointdistance
                        #print('Case 0 move north')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 1 #lastDirection arrugment (1,2,3,4) => (N,W,S,E) 

                #Case 5 move west from corner
                elif self.north == 1 and self.northEast == 1 and self.southEast == 1 and self.west == 0: #may be better to change north to north west, but its not broken of mi no going to fix it.
                    '''          This is an example of the scanned logic and required quardrant responses. T is object full, F is no object, W is waypoint direction. blank spots are not checked
                         TT
                       WF* 
                          T'''
                    wayX = self.currentX - self.wayPointdistance
                    wayY = self.currentY 
                    if self.northClose ==  1:
                        wayY = self.currentY -1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 2
                    #print('Case 5 move west')
                    
                #Case 6 move south from corner
                elif self.west == 1 and self.northWest == 1 and self.north == 1 and self.south == 0:
                    wayX = self.currentX 
                    wayY = self.currentY - self.wayPointdistance
                    if self.westClose == 1:
                        wayX = self.currentX + 1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 3
                    #print('Case 6 move south')
                
                #Case 7 move east from corner
                elif self.west == 1 and self.southWest == 1 and self.south == 1 and self.east == 0:
                    wayX = self.currentX + self.wayPointdistance
                    wayY = self.currentY 
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 4
                    if self.southClose == 1:
                        wayY = self.currentY + 1
                        ##print('close')
                    #print('Case 7 move east')

                #Case 8 move north from corner
                elif self.south == 1 and self.southEast == 1 and self.east == 1 and self.north == 0:
                    wayX = self.currentX 
                    wayY = self.currentY + self.wayPointdistance
                    if self.eastClose == 1:
                        wayX = self.currentX - 1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 1
                    #print('Case 8 move north')
                
                #Case 1 move north
                elif self.north == 0 and ( self.northEast == 1 or self.east == 1 )and self.west == 0: 
                    ''' W          This is an example of the scanned logic and required quardrant responses. T is object full, F is no object, W is waypoint direction. blank spots are not checked
                        FT
                       F*T
                       '''
                    wayX = self.currentX 
                    wayY = self.currentY + self.wayPointdistance
                    if self.eastClose == 1:
                        wayX = self.currentX - 1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 1
                    #print('Case 1 move north')        
                
                #Case 2 move west
                elif self.west == 0 and ( self.northWest == 1 or self.north == 1 )and self.south ==  0 : 
                    wayX = self.currentX - self.wayPointdistance
                    wayY = self.currentY 
                    if self.northClose ==  1:
                        wayY = self.currentY -1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 2
                    #print('Case 4 move west')
                    
                #Case 3 move south
                elif self.south == 0 and ( self.southWest == 1 or self.west == 1 ) and self.east == 0 : 
                    wayX = self.currentX 
                    wayY = self.currentY - self.wayPointdistance
                    if self.westClose == 1:
                        wayX = self.currentX + 1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 3
                    #print('Case 3 move south')
                
                #case 4 move east
                elif self.east == 0 and ( self.southEast == 1 or self.south == 1 ) and self.north == 0 : 
                    wayX = self.currentX + self.wayPointdistance
                    wayY = self.currentY 
                    if self.southClose == 1:
                        wayY = self.currentY + 1
                        ##print('close')
                    self.wayPointSteps = [wayX,wayY]
                    self.lastDirection = 4
                    #print('Case 4 move east')
                
                if (self.twoStepsBack == 2 and self.lastDirection == 4) or (self.twoStepsBack == 4 and self.lastDirection == 2) or (self.twoStepsBack == 1 and self.lastDirection == 3) or (self.twoStepsBack == 3 and self.lastDirection == 1):
                    self.explorerFlag = 1
                    self.explorerCounter = 0
                    ##print('last move backtrack=> explorer')
                #************************
                #These case work based on the previous direction of travel. To deal with doors and so on.
                #************************
                #case 9 north/south door*****************
                elif (self.west == 1 ) and (self.east == 1 ): 
                    '''  W          This is an example of the scanned logic and required quardrant responses. T is object full, F is no object, W is waypoint direction. blank spots are not checked
                        T*T
                          '''
                    if self.lastDirection == 1 and self.north ==0:
                        wayX = self.currentX 
                        wayY = self.currentY + self.wayPointdistance
                        self.wayPointSteps = [wayX,wayY]
                        #print('Case 9 move north')
                        
                    elif self.south == 0:
                        self.lastDirection = 3
                        wayX = self.currentX 
                        wayY = self.currentY - self.wayPointdistance
                        self.wayPointSteps = [wayX,wayY]
                        #print('Case 9 move south')
                
                #case 10 east/west door*****************
                elif (self.north == 1 ) and (self.south == 1):#added lastDirection arrugment 1,2,3,4 (N,W,S,E) 
                    '''  T
                         *W
                         T'''
                    if self.lastDirection == 4 and self.east ==0:
                        wayX = self.currentX + self.wayPointdistance
                        wayY = self.currentY 
                        self.wayPointSteps = [wayX,wayY]
                        #print('Case 10 move east')
                        
                    elif self.west ==0:
                        self.lastDirection = 2
                        wayX = self.currentX - self.wayPointdistance
                        wayY = self.currentY 
                        self.wayPointSteps = [wayX,wayY]
                        #print('Case 10 move west') 
                  
            else:
                explorerFlag = 1
                explorerCounter = 0
                self.nothingHappened = 1
                #print('nothing happened normal')
        elif [navMain.currentX,navMain.currentY]==[navMain.wayPointSteps[0],navMain.wayPointSteps[1]]:
            '''
            If the waypoint is the same as the robot location the waypoint is updated in next cycle
            '''
            self.nothingHappened = 1
            print('nothing happened updatewaypoint')
            
        #Robot navigation History 
        '''
        This ensures that the map does not update until the robot has moved or a new object is found in an a quadrant that has not been triggered yet. This means that my simulations 
        will be correct since the robot will move toward the waypoint one quadrant before the next waypoint is set.
        '''
        self.lastPosition = [self.currentX,self.currentY]
        self.lastNorth = self.north 
        self.lastNorthWest= self.northWest 
        self.lastWest = self.west 
        self.lastSouthWest = self.southWest 
        self.lastSouth = self.south 
        self.lastEast = self.east
        self.lastNorthEast = self.northEast
        self.lastNorthClose = self.northClose
        self.lastWestClose = self.westClose 
        self.lastSouthClose = self.southClose 
        self.lastEastClose = self.eastClose
        self.lastExplorerNorth = self.explorerNorth
        self.lastExplorerWest = self.explorerWest 
        self.lastExplorerSouth = self.explorerSouth 
        self.lastExplorerEast = self.explorerEast 
        
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
    mapHeight = 5        #30      #5        # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
    mapWidth =  5        #30      #5        # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
    resolution = .305*.5 #.305*.5 # .305*.5 #.302#Test with .5 #meters Even fraction Note: see previous note 
        
    #Test scan array********************************************************
    class scanMain():
        pass
        #print('scan Object created')

    #*************************************************************************************************
    #  Test navigation assumes Robot only makes it 2 feet from its current waypoint before its updated
    #*************************************************************************************************
    #******************************************************************
    #Set Prompt height to 9999 when printing maps 123-146 maps!!!!!!!!
    #******************************************************************
    
    
    crazy = 1 # did to set promp height to atleast 5000???
    
    if crazy == 1: 
        '''
        Only cray people would print a 66x66 character map to screen 123 times 
        '''
        mapHeight = 10        # 10#30      #5        # 40 #Test with 10 #meters (height) Ensure whole numbers 20X20,10x10,11x11, 11x9 I want to avoid  10.5x10.5
        mapWidth =  10        #10 #30      #5        # 40 #Test with 10 #meters (witth) Note: base 2 would be best 2 ,4, 6, who....
        resolution = .302*.5  #.305*.5     #.305*.5 # .305*.5 #.302#Test with .5 #meters Even fraction Note: see previous note 
        
        X = 31*resolution  # 31*resolution#14*resolution
        Y =-12*resolution  #-12*resolution #resolution*-7
        
        dictionary = {'positionX': X, 'positionY':Y} 
        
        scanMain.posX=array.array('f',[x*resolution for x in [6,7,10,10,10,10,0,1,12,-10, -10,-11,-12,-10,-10,11,12,13,5,0,0,-10,32,22,30,20,28,26,24,18,16,14,12,10,28,31,26,29,28,0,0,-2,-4,-12,-12,-14,-14,-30,-28,-26,-24,-24,-24,-24,-30,-28,-26,-24,-24,-24,-24,9,7,3,3,10,10,10,9,15,16,17,18,0,-2,-3,-2,0,10,12,14,16]])
        scanMain.posY=array.array('f',[y*resolution for y in [3,3,10,11,12,10,0,1,0,0,-6,-6,-6,-9,-11,-9,-9,-9,-3,-8,-7,3,-7,-7,-7,-7,-7,-7,-7,-7,-7,-7,-5,-3,10,12,14,16,18,-3,31,29,31,31,29,31,29,0,0,0,0,2,4,6,-6,-6,-6,-6,-8,-10,-12,1,-3,-3,2,9,7,5,4,30,30,30,30,-30,-29,-27,-25,-24,-31,-29,-27,-25]])    
        scanMain.headingPlusServoAngle=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note we could combine the angles in sensing.    
        scanMain.distance=array.array('f',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #Note I antisipate that we will choose between the two IR sensers close and far range using range limits and returing that distance. So sensing converts the raw data.    
        mapMain = mapping.mapObj(mapHeight, mapWidth, resolution)
        navMain = navObj(mapHeight, mapWidth, resolution)
        #print('scan width 0000000',round(7*resolution,2),'m',round(7*resolution*3.28,2),'ft') 
         
        mapMain.writeMap(scanMain)
        counter = 0
        nothingHappenedCounter = 0
        navMain.wayPointdistance = 1
        
        numberOfIterations = 1   #146#123 at 9999
        
        while counter < numberOfIterations: 
            ##print('\nIteration', counter, '***************************************************')
            navMain.navTask(dictionary)
            mapMain.printMapFancy(dictionary,0,0)
            dictionary = {'positionX': navMain.wayPoint[0], 'positionY':navMain.wayPoint[1]}
            counter +=1
            #print('position',[navMain.currentX,navMain.currentY],'wayPoint',[navMain.wayPointSteps[0],navMain.wayPointSteps[1]])  
            #print('north',navMain.north)
            #print('northWest',navMain.northWest)
            #print('west',navMain.west)
            #print('southWest',navMain.southWest)
            #print('south',navMain.south)
            #print('east',navMain.east)
            #print('northEast',navMain.northEast)
            #print('northclose',navMain.northClose)
            #print('westClose',navMain.westClose)
            #print('southClose',navMain.southClose)
            #print('eastClose',navMain.eastClose)
            #print('explorerNorth',navMain.explorerNorth)
            #print('explorerWest',navMain.explorerWest)
            #print('explorerSouth',navMain.explorerSouth)
            #print('exploroerEast',navMain.explorerEast)
            #print('nothingHappended',navMain.nothingHappened)
            if navMain.nothingHappened == 1:
                nothingHappenedCounter +=1
        
        print('#ofnothingHappens',nothingHappenedCounter,'in ', numberOfIterations, 'iterations')
        #Results 2 in 1000 steps so very small probability of this problem.
        
        
        
        
        #Testing memory Usage******************************************************************************************************************************************************
        
        import sys
        
        print('\nMemory Test******************************************')
        print('navMain',sys.getsizeof(navMain))
        print('navMain.setWayPoint',sys.getsizeof(navMain.setWayPoint))
        print('navMain.scanMap',sys.getsizeof(navMain.scanMap))
        print('scanMain',sys.getsizeof(scanMain))
        print('scanMain.posX',sys.getsizeof(scanMain.posX))
        
        
        northCheckList =        [[-1,3],[0,3],[1,3],[-1,2],[0,2],[1,2],[-1,1],[0,1],[1,1]]
        westCheckList =         [[-3,1],[-2,1],[-1,1],[-3,0],[-2,0],[-1,0],[-3,-1],[-2,-1],[-1,-1]]
        southCheckList =        [[-1,-3],[0,-3],[1,-3],[-1,-2],[0,-2],[1,-2],[-1,-1],[0,-1],[1,-1]]
        eastCheckList =         [[3,1],[2,1],[1,1],[3,0],[2,0],[1,0],[3,-1],[2,-1],[1,-1]]
        
        explorerNorthCheckList =        [          [2,0],[2,1],[2,1]]        #,[-2,0],[-2,1],[-2,2]
        explorerWestCheckList =         [        [0,2],[-1,2],[-2,2]]        #,[0,-2],[-1,-2],[-2,-2]
        explorerSouthCheckList =        [     [-2,0],[-2,-1],[-2,-2]]        #,[2,0],[2,-1],[2,-2]
        explorerEastCheckList =         [       [0,-2],[1,-2],[2,-2]]        #[0,2],[1,2],[2,2],
        
        northWestCheckList =    [[-3,3],[-2,3],[-3,2],[-2,2],[-1,2],[-2,1],[-1,1]]#,[0,1],[-1,0]]
        southWestCheckList =    [[-3,-3],[-2,-3],[-3,-2],[-2,-2],[-1,-2],[-2,-1],[-1,-1]]#,[0,-1],[-1,0]]
        southEastCheckList =    [[3,-3],[2,-3],[3,-2],[2,-2],[1,-2],[2,-1],[1,-1]]#,[0,-1],[1,0]]
        northEastCheckList =    [[3,3],[2,3],[3,2],[2,2],[1,2],[2,1],[1,1]]#,[0,1],[1,0]]
        
        #These check if the robot is directly by the wall and logic tries to move robot to be atleast 1 element way from wall
        northCloseCheck =       [[0,1]]     #[[-1,1],[0,1],[1,1]]
        westCloseCheck =        [[-1,0]]    #[[-1,-1],[-1,0],[-1,1]]
        southCloseCheck =       [[0,-1]]    #[[-1,-1],[0,-1],[1,-1]]
        eastCloseCheck =        [[1,0]]     #[[1,-1],[1,0],[1,1]]
        
        
        print('northCheckList', sys.getsizeof(westCheckList))
        print('westCheckList', sys.getsizeof(westCheckList))
        print('southWestCheckList', sys.getsizeof(westCheckList))
        
        
        
        
        
