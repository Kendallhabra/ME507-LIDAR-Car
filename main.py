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
import encoder
import statusLight

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
# motorB = pyb.Pin("Motor PWM B", pyb.Pin.OUT_PP)
motorA.value(0)
# motorB.value(1)

mtrPower = 0
mtrPowerDir = 1

mtrTimer = pyb.Timer(4, freq = 1000)
mtrPWM = mtrTimer.channel(2, pyb.Timer.PWM, pin = pins["Motor PWM B"])
mtrPWM.pulse_width_percent(0)

encoderTask = encoder.EncoderTask(pins["Encoder A"], pins["Encoder B"])
positionTask = position.PositionTask(encoderTask)
statusLightTask = statusLight.StatusLightTask(pins["LED R"], pins["LED G"], pins["LED B"])

def coerce(x, a, b):
	return min(b, max(x, a))

mode = 0
def setMode(newMode):
	global mode
	mode = newMode
	print(mode)

def startMode(line):
	global mode
	mode = 1
	print(mode)

def stopMode(line):
	global mode
	if mode == 0:
		encoderTask.count = 0
		positionTask.pos["x"] = 0
        positionTask.pos["y"] = 0
	mode = 0
	print(mode)

ext = pyb.ExtInt(pins["Start Btn"], pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, startMode)
ext = pyb.ExtInt(pins["Stop Btn"], pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, stopMode)

batVoltageADC = pyb.ADC(pins["Battery Voltage"])
batVoltage = 0

bluetooth = pyb.UART(2, 9600)
bluetooth.init(9600, bits=8, parity=None, stop=1)

servoAngle = 45
servoHead = pyb.Servo(1)
servoSteer = pyb.Servo(2)

servoHead.angle(0)
servoSteer.angle(0)

def randInt(a, b):
	return int(pyb.rng()*((b-a)/1073741824)+a)

def read():
#	print(positionTask.pos["x"], ", ", positionTask.pos["y"])
	#print(bno.read_euler())
	#print(bno.read_quaternion())
	pass
def setMotor():
	global mtrPower, mtrPowerDir
	if batVoltage < 5 or mode == 0:
		mtrPower = 0
		mtrPowerDir = 1
		mtrPWM.pulse_width_percent(0)
		return

	if mtrPower == 100:
		mtrPowerDir = -1
	elif mtrPower == 0:
		mtrPowerDir = 1
	mtrPower += mtrPowerDir
	mtrPWM.pulse_width_percent(50)
def encCounts():
	print("Encoder Counts:", encoderTask.count)
def toggleLED():
	pyb.LED(4).toggle()
def sayHello():
	#print("Hello world!")
	#print(str(randInt(0, 255)))
	bluetooth.write("<")
	#bluetooth.write(str(randInt(0, 255)))
	bluetooth.write(str(int(positionTask.pos["x"])))
	bluetooth.write(",")
	#bluetooth.write(str(randInt(0, 255)))
	bluetooth.write(str(int(positionTask.pos["y"])))
	bluetooth.write(",")
	bluetooth.write("255")
	bluetooth.write(",")
	bluetooth.write(str(int(positionTask.pos["heading"])))
	bluetooth.write(">")
	#bluetooth.write("\033[")
	# <c#,#,#,#>
def sayTime():
	pass
	# print(pyb.millis())
def garbageCollect():
	gc.collect()
def setServo():
	global servoAngle
	if batVoltage < 5:
		return
	servoHead.angle(servoAngle)
	servoAngle = 0 - servoAngle
def getVoltage():
	global batVoltage
	batVoltage = batVoltageADC.read() * 0.00447
	print("Battery Voltage:", batVoltage)

def setLight():
	statusLightTask.r = (statusLightTask.r + randInt(0, 101))/2
	statusLightTask.g = (statusLightTask.g + randInt(0, 101))/2
	statusLightTask.b = (statusLightTask.b + randInt(0, 101))/2

# Each list in tasks holds [function, period in ms, calls, priority].
# Calls starts at 0 and is used to control function calls.
# Setting a higher priority will overwrite a lower priority in a given call of mainLoop.
tasks = [
#	[read, 1000, 0, 0],
	[encCounts, 5000, 0, 5],
	[toggleLED, 100, 0, 10],
	[sayHello, 500, 0, 5],
	[sayTime, 2000, 0, 5],
	[garbageCollect, 1000, 0, 1],
	[getVoltage, 5000, 0, 5],
	[positionTask.run, 10, 0, 5],
	[statusLightTask.run, 10, 0, 0],
	[setMotor, 100, 0, 5],
	[setLight, 10, 0, 5],
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
