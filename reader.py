#Zachary Arnott

#Read saved maps
import os
import re
import tkinter


'''
Creates the map first time map is run and ajusts the array size (lenght and width) in the case that they are not interger values.
'''
saveMapFlag = 0
        
        
#Create an intial timer count
if __name__ != '__main__' and os.getcwd() =='/':
    saveMapInterval = 10000 #ms or 10 seconds till next save
    runTime = pyb.millis() + saveMapInterval

       
        
def reader(): #!!!!!!!!!!!!may not work in micro python!!!!!!!!!!!!!!!!!!
        '''
        Prints the Map in the best readable formate I have found so far without 3rd party modules
        '''
        # print('\n********************Printing map*********************\n')
        # print('Map width:',round(numberOfCol*resolution,1),'m Map Length:', round(numberOfRows*resolution,1),'m Resolution', round(resolution,4),'m\n')
        # print('Map width:',round(numberOfCol*resolution*3.28,1),'ft Map Length:', round(numberOfRows*resolution*3.28,1),'ft Resolution', round(resolution*3.28,4),'ft\n')
        # print('Extremes array units(bitmap units): \n(',-numberColumnLeft,numberRowAboveOrgin,') (',numberColumnRight,numberRowAboveOrgin,') (',numberColumnRight,-numberRowBlowOrgin,') (',-numberColumnLeft,-numberRowBlowOrgin,')\n')
        # print('Extremes in meters:\n(',round(-numberColumnLeft*resolution,1),round(numberRowAboveOrgin*resolution,1),') (',round(numberColumnRight*resolution,1),round(numberRowAboveOrgin*resolution,1),') (',round(numberColumnRight*resolution,1),round(-numberRowBlowOrgin*resolution,1),') (',round(-numberColumnLeft*resolution,1),round(-numberRowBlowOrgin*resolution,1),')\n')
        # print('Extremes in feet:\n(',round(-numberColumnLeft*resolution*3.28,1),round(numberRowAboveOrgin*resolution*3.28,1),') (',round(numberColumnRight*resolution*3.28,1),round(numberRowAboveOrgin*resolution*3.28,1),') (',round(numberColumnRight*resolution*3.28,1),round(-numberRowBlowOrgin*resolution*3.28,1),') (',round(-numberColumnLeft*resolution*3.28,1),round(-numberRowBlowOrgin*resolution*3.28,1),')\n')
        Filetrueorfalse = 0
        
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
            # print(numberOfElements)
            # print(numberOfRows)
            # print('numberOfRows',numberOfRows)
        
        mapPixels = 4 #number of pixels for each quadrant
        
        root = tkinter.Tk()
        canvas = tkinter.Canvas(root)
        canvas.pack()
        canvas.config(width=numberOfRows*mapPixels-2, height=numberOfCol*mapPixels-2)
        
        
        iterateCol = 0
        iterateRow = 0
        exitFlag = 0
        
        while exitFlag == 0:
            '''
            Iterates through each bit printing only the bit with no spaces. 
            '''
            #print('running')
            if   map[iterateRow*numberOfCol+iterateCol] == '*':
                #print('*******************************************')
                '''
                If the Robot is the current data point then it prints the robot character '*'
                '''
                rect = canvas.create_rectangle(mapPixels*iterateCol   ,mapPixels*iterateRow   ,   mapPixels*(iterateCol+1)   ,   mapPixels*(iterateRow +1)  , outline="black", fill="red")
            elif map[iterateRow*numberOfCol+iterateCol]== '1':
                rect = canvas.create_rectangle(mapPixels*iterateCol   ,mapPixels*iterateRow   ,   mapPixels*(iterateCol+1)   ,   mapPixels*(iterateRow +1)  , outline="black", fill="white")
                #print('111111111111111111111111111111111111111')
            else:
                #print('0')
                rect = canvas.create_rectangle(mapPixels*iterateCol   ,mapPixels*iterateRow   ,   mapPixels*(iterateCol+1)   ,   mapPixels*(iterateRow +1)  , outline="black", fill="black")

            iterateCol +=1
            
            if (iterateRow+1)*(iterateCol) == numberOfElements:
                '''
                If map complete we exit
                '''
                exitFlag = 1
            elif iterateCol == numberOfCol:
                '''
                otherwise if the end of a row has been reached we move to the next row
                '''
                iterateRow +=1 
                iterateCol = 0
            
        
        return           
        
reader()

        
        
