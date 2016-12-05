# Main Python File

'''
Main
This file does a thing...
'''

import time
import pyb
import micropython
import gc

import position

micropython.alloc_emergency_exception_buf(100)


pins = {
	"Start Btn": pyb.Pin.board.Y1,
	"Stop Btn": pyb.Pin.board.Y2,
	"IMU Reset": pyb.Pin.board.Y3,
	"Motor Error": pyb.Pin.board.Y4,
	"LED R": pyb.Pin.board.Y6,
	"LED G": pyb.Pin.board.Y7,
	"LED B": pyb.Pin.board.Y8,
	"SCL": pyb.Pin.board.Y9,
	"SDA": pyb.Pin.board.Y10,
	"Encoder A": pyb.Pin.board.Y11,
	"Encoder B": pyb.Pin.board.Y12,
	"Servo Head": pyb.Pin.board.X1,
	"Servo Steer": pyb.Pin.board.X2,
	"Serial TX": pyb.Pin.board.X3,
	"Serial RX": pyb.Pin.board.X4,
	"Rangefinder 1": pyb.Pin.board.X5,
	"Rangefinder 2": pyb.Pin.board.X6,
	"Rangefinder 3": pyb.Pin.board.X7,
	"Rangefinder 4": pyb.Pin.board.X8,
	"Motor PWM A": pyb.Pin.board.X9,
	"Motor PWM B": pyb.Pin.board.X10,
	"Battery Voltage": pyb.Pin.board.X11,
	"Bumb Sensor 2": pyb.Pin.board.X19,
	"Bumb Sensor 1": pyb.Pin.board.X20,
	"Rangefinder 6": pyb.Pin.board.X21,
	"Rangefinder 5": pyb.Pin.board.X22,
}


pyb.Pin.dict(pins)
motorA = pyb.Pin("Motor PWM A", pyb.Pin.OUT_PP)
motorB = pyb.Pin("Motor PWM B", pyb.Pin.OUT_PP)
motorA.value(0)
motorB.value(1)


#bno = imu.BNO055()
#print(bno.begin())

servoAngle = 45
servoHead = pyb.Servo(1)
servoSteer = pyb.Servo(2)

# servoSteer.angle(servoAngle)

positionTask = position.PositionTask()

def read():
	print(positionTask.pos[x], ", ", positionTask.pos[y])
	#print(bno.read_euler())
	#print(bno.read_quaternion())
	pass
def toggleLED():
	pyb.LED(4).toggle()
def sayHello():
	print("Hello world!")
def sayTime():
	pass
	# print(pyb.millis())
def garbageCollect():
	gc.collect()
def setServo():
	global servoAngle
	servoHead.angle(servoAngle)
	servoAngle = 0 - servoAngle
	
	




# Each list in tasks holds [function, period in ms, calls, priority].
# Calls starts at 0 and is used to control function calls.
# Setting a higher priority will overwrite a lower priority in a given call of mainLoop.
tasks = [
	[read, 1000, 0, 0],
	[toggleLED, 100, 0, 1],
	[sayHello, 100000, 0, 0],
	[sayTime, 2000, 0, 0],
	[garbageCollect, 1000, 0, 0],
	[positionTask.run(), 10, 0, 0],
#	[setServo, 2000, 0, 0],
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
