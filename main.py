# Main Python File

'''
Main
This file does a thing...
'''

import time
import pyb
import micropython
import gc
import imu

micropython.alloc_emergency_exception_buf(100)

bno = imu.BNO055()
print(bno.begin())

def read():
	print(bno.read_euler())
	print(bno.read_quaternion())
def toggleLED():
	pyb.LED(4).toggle()
def sayHello():
	print("Hello world!")
def sayTime():
	pass
	# print(pyb.millis())
def garbageCollect():
	gc.collect()

# Each list in tasks holds [function, period in ms, calls, priority].
# Calls starts at 0 and is used to control function calls.
# Setting a higher priority will overwrite a lower priority in a given call of mainLoop.
tasks = [
	[read, 3000, 0, 0],
	[toggleLED, 100, 0, 1],
	[sayHello, 100000, 0, 0],
	[sayTime, 2000, 0, 0],
	[garbageCollect, 1000, 0, 0],
	]

def mainLoop():
	global tasks
	tasksToRun = []
	highestPriority = 0
	curTime = pyb.millis()
	for taskNum, task in enumerate(tasks):
		if int(curTime/task[1]) > task[2]:
			tasksToRun.append(taskNum)
			highestPriority = max(highestPriority, task[3])
	for taskNum in tasksToRun:
		if tasks[taskNum][3] == highestPriority:
			tasks[taskNum][0]()
			tasks[taskNum][2] = int(curTime/tasks[taskNum][1])

gc.collect()




print("Running")
while(True):
	mainLoop()
	#pyb.delay(1)
'''
tim = pyb.Timer(4, freq=10)
tim.callback(lambda t: mainLoop)

'''
