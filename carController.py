import time
import serial
import sys
import pygame
import tkinter as tk
import re

# Sets up main window.

mainWindow = tk.Tk()
mainWindow.geometry("640x600")

# Creates text widgets for each button on the joystick.

ROW_1 = 10
ROW_2 = 30
ROW_3 = 50

CONT_X = 10
CONT_Y = 10

BUTTON_ROW = 150

CANVAS_WIDTH = 325
CANVAS_HEIGHT = 325

selectText = tk.Text(mainWindow, height = 1, width = 3)
selectText.place(x = CONT_X + 55, y = CONT_Y + ROW_2)
selectText.insert("1.0", "Sel")

startText = tk.Text(mainWindow, height = 1, width = 3)
startText.place(x = CONT_X + 100, y = CONT_Y + ROW_2)
startText.insert("1.0", "Sta")

upText = tk.Text(mainWindow, height = 1, width = 1)
upText.place(x = CONT_X + 15, y = CONT_Y + ROW_1)
upText.insert("1.0", "U")

rightText = tk.Text(mainWindow, height = 1, width = 1)
rightText.place(x = CONT_X + 30, y = CONT_Y + ROW_2)
rightText.insert("1.0", "R")

downText = tk.Text(mainWindow, height = 1, width = 1)
downText.place(x = CONT_X + 15, y = CONT_Y + ROW_3)
downText.insert("1.0", "D")

leftText = tk.Text(mainWindow, height = 1, width = 1)
leftText.place(x = CONT_X, y = CONT_Y + ROW_2)
leftText.insert("1.0", "L")

triangleText = tk.Text(mainWindow, height = 1, width = 1)
triangleText.place(x = CONT_X + 155, y = CONT_Y + ROW_1)
triangleText.insert("1.0", "∆")

circleText = tk.Text(mainWindow, height = 1, width = 1)
circleText.place(x = CONT_X + 170, y = CONT_Y + ROW_2)
circleText.insert("1.0", "O")

squareText = tk.Text(mainWindow, height = 1, width = 1)
squareText.place(x = CONT_X + 140, y = CONT_Y + ROW_2)
squareText.insert("1.0", "□")

xText = tk.Text(mainWindow, height = 1, width = 1)
xText.place(x = CONT_X + 155, y = CONT_Y + ROW_3)
xText.insert("1.0", "X")

speedText = tk.Text(mainWindow, height = 1, width = 20)
speedText.place(x = CONT_X + 55, y = CONT_Y + ROW_3 + 30)
speedText.insert("1.0", "Speed: 0")

angleText = tk.Text(mainWindow, height = 1, width = 20)
angleText.place(x = CONT_X + 55, y = CONT_Y + ROW_3 + 60)
angleText.insert("1.0", "Angle: 0")

# Creates entry boxes in the main window.

entrySerial = tk.Entry(mainWindow, width = 20)
entrySerial.place(x = 10, y = BUTTON_ROW + 20)
entrySerial.insert(1, "usbserial-A6005Jeq")

entryCommand = tk.Entry(mainWindow, width = 20)
entryCommand.place(x = 10, y = BUTTON_ROW + 280)
entryCommand.insert(1, "")

# Defines look-up dictionaries for the joystick and serial commands.

analogCommands = {
	"angle": b"a",
	"distance": b"d",
	"lineDist": b"l",
	"radius": b"r",
	"speed": b"s",
	"lineSpeed": b"v",
}

digitalCommands = {
	0: [b"c", selectText],
	3: [b"z", startText],
	4: [b"n", upText],
	5: [b"p", rightText],
	6: [b"b", downText],
	7: [b"q", leftText],
	12: [b"j", triangleText],
	13: [b"o", circleText],
	14: [b"m", xText],
	15: [b"", squareText],
}

sticks = {
	"Left Vertical": 1,
	"Left Horizontal": 0,
	"Right Vertical": 3,
	"Right Horizontal": 2,
}

'''
# Configures the serial connection to the robot via either Bluetooth or USB.
ser = serial.Serial(
	"/dev/tty.HC-06-DevB",
	baudrate = 9600,
	timeout = 0,
	writeTimeout = 0,
	)
'''
# Initializes the serial port and controller.
ser = None
PS3 = None

pygame.init()

# Configures the serial connection to the robot via either Bluetooth or USB.


def connectSerial():
	global ser

	try:
		ser = serial.Serial(
			"/dev/tty." + entrySerial.get(),
			# baudrate = 115200,
			baudrate = 9600,
			timeout = 0,
			writeTimeout = 0,
			)
	except:
		print("USB Serial Error.   Trying Bluetooth Serial.")
		try:
			ser = serial.Serial(
				"/dev/tty.HC-06-DevB",
				#baudrate = 115200,
				baudrate = 9600,
				timeout = 0,
				writeTimeout = 0,
				)
		except:
			print("Bluetooth Serial Error.")
			ser = None

def connectController():
	global PS3

	try:
		if pygame.joystick.get_count() >= 0:
			PS3 = pygame.joystick.Joystick(0)
			PS3.init()
		else:
			print("No Controllers Detected.")
			PS3 = None
	except:
		print("PS3 Controller Error.")
		ser = None



# Checks the robot's status from the serial buffer.
getStatus = False
sendControl = True

MAX_ANGLE = 6400 # hundredths of a degree
MAX_SPEED = -32767 # hundredths of a degree

delNext = False

def addPixel(x, y, val):
	_x = int(x/50 + 127)
	_y = int(y/50 + 127)

	color = "#" + '{:02x}'.format(val) + '{:02x}'.format(val) + '{:02x}'.format(val)
	img.put(color, (coerce(_x, 0, 255), coerce(_y, 0, 255)))

def coerce(x, a, b):
	return min(b, max(x, a))

def angMap(angle):
	if (angle < 0):
		sign = -1
	else:
		sign = 1
	return sign*(angle**2)

serBuffer = ""

def comm():
	global delNext
	global serBuffer

	buttons = b""

	pygame.event.pump()
	if PS3 is None:
		connectController()
		for buttonNum, buttonInfo in digitalCommands.items():
			buttonInfo[1].config(bg = "firebrick1")
		speed = 0
		angle = 0
	else:
		for buttonNum, buttonInfo in digitalCommands.items():
			if PS3.get_button(buttonNum):
				buttonInfo[1].config(bg = "blue")
				buttons += buttonInfo[0]
			else:
				buttonInfo[1].config(bg = "green3")
		speed = int(MAX_SPEED*PS3.get_axis(sticks["Right Vertical"]))
		angleRaw = PS3.get_axis(sticks["Right Horizontal"])
		angle = int(MAX_ANGLE*angMap(angleRaw))
	
	speedText.delete(1.0, tk.END)
	angleText.delete(1.0, tk.END)

	speedText.insert(1.0, "Speed: " + str(speed))
	angleText.insert(1.0, "Angle: " + str(angle))

	
	# Gets status and sends
	if (ser is not None):
		count = 0
		
		try:
			text = str(ser.read(ser.inWaiting()), "utf-8").replace("\r\n", "\n")
			
			serBuffer += text

			if ">" in serBuffer:
				log.delete(1.0, tk.END)
				log.insert(1.0, serBuffer)

				stringSplit = serBuffer.split(">", 1)
				if "<" in stringSplit[0]:
					vals = stringSplit[0].split("<", 1)[1].split(",")
					addPixel(int(vals[0]), int(vals[1]), int(vals[2]))
				serBuffer = stringSplit[-1] if len(stringSplit) > 1 else ""

			# <p,#,#>

			'''
			length = serBuffer.find("\033[")
			endLength = serBuffer.rfind("\033[")
			if (length >= 0):
				log.delete(1.0, tk.END)
				log.insert(1.0, serBuffer[:length])
				serBuffer = serBuffer[(endLength + 5):]
			'''
			'''
			start = text.find("Run Mode:")
			length = text.find("\033[")
			if ((length >= 0) and (start == 0)):
				log.delete(1.0, tk.END)
				log.insert(1.0, text[:length])
			else:
				print("Invalid Packet.")
			'''
		except:
			print("Serial Read Error.")

		# try:
		ser.flush()
		if sendControl:
			ser.write(buttons)
			sendAnalog("angle", angle)
			sendAnalog("speed", speed)

		# Sends the command to get the status over serial.
		ser.write(b'i')
		# except:
		#	print("Serial Write Error.")
	
	mainWindow.after(20, comm)


def clearSerial():
	global serBuffer
	serBuffer = ""
	log.delete(1.0, tk.END)

def toggleSend():
	global sendControl
	sendControl = not sendControl;

def sendAnalog(variable, value):
	if (variable in analogCommands):
		ser.write(analogCommands[variable])
		ser.write(str.encode(str(value)))
		ser.write(b";")

def sendCommand():
	ser.write(str.encode(entryCommand.get()))

def sendChar(char):
	if ser is not None:
		try:
			ser.write(char)
		except:
			print("Serial Write Error on Character: " + char)

# Creates the serial log for the main window.
log = tk.Text(mainWindow, height = 14, width = 50)
log.place(x = 250, y = ROW_1)

# Creates the canvas for the map.
canvas = tk.Canvas(mainWindow, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#000000")
canvas.place(x = 248, y = 250)
img = tk.PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.create_image((CANVAS_WIDTH/2, CANVAS_HEIGHT/2), image=img, state="normal")

'''
entrySpeed = tk.Entry(mainWindow, width = 30)
entrySpeed.place(x = 120, y = 170)

buttonFaster = tk.Button(mainWindow, text = "Faster", command = faster)
buttonFaster.place(x = 10, y = 10, width = 100, height = 30)

buttonSlower = tk.Button(mainWindow, text = "Slower", command = slower)
buttonSlower.place(x = 10, y = 50, width = 100, height = 30)

buttonStatus = tk.Button(mainWindow, text = ON_TEXT, command = toggleStatus)
buttonStatus.place(x = 10, y = 90, width = 100, height = 30)

buttonReset = tk.Button(mainWindow, text = "Zero", command = lambda: sw(b"z"))
buttonReset.place(x = 10, y = 130, width = 100, height = 30)

buttonSet = tk.Button(mainWindow, text = "Set Speed", command = setSpeed)
buttonSet.place(x = 10, y = 170, width = 100, height = 30)
'''

# Creates buttons to control the program.
labelSerial = tk.Label(mainWindow, width = 20, text = "Serial Port:", anchor = tk.W)
labelSerial.place(x = 10, y = BUTTON_ROW)

buttonSerial = tk.Button(mainWindow, text = "Connect Serial", command = connectSerial)
buttonSerial.place(x = 10, y = BUTTON_ROW + 50, width = 120, height = 30)

buttonToggleSend = tk.Button(mainWindow, text = "Toggle Send", command = toggleSend)
buttonToggleSend.place(x = 10, y = BUTTON_ROW + 80, width = 120, height = 30)

buttonToggleSimple = tk.Button(mainWindow, text = "Toggle Simple", command = lambda: sendChar(b"k"))
buttonToggleSimple.place(x = 10, y = BUTTON_ROW + 110, width = 120, height = 30)

buttonToggleGhost = tk.Button(mainWindow, text = "Toggle Ghost", command = lambda: sendChar(b"g"))
buttonToggleGhost.place(x = 10, y = BUTTON_ROW + 140, width = 120, height = 30)

buttonClearSerial = tk.Button(mainWindow, text = "Clear Serial", command = lambda: clearSerial())
buttonClearSerial.place(x = 10, y = BUTTON_ROW + 170, width = 120, height = 30)

buttonRadius2 = tk.Button(mainWindow, text = "Set Radius - 30", command = lambda: sendAnalog("radius", 30))
buttonRadius2.place(x = 10, y = BUTTON_ROW + 200, width = 120, height = 30)

buttonRadius3 = tk.Button(mainWindow, text = "Set Radius - 42", command = lambda: sendAnalog("radius", 42))
buttonRadius3.place(x = 10, y = BUTTON_ROW + 230, width = 120, height = 30)

labelCommand = tk.Label(mainWindow, width = 20, text = "Serial Command:", anchor = tk.W)
labelCommand.place(x = 10, y = BUTTON_ROW + 260)

buttonCommand = tk.Button(mainWindow, text = "Send Command", command = sendCommand)
buttonCommand.place(x = 10, y = BUTTON_ROW + 310, width = 120, height = 30)


# Runs the main communication and window loops.
mainWindow.after(100, comm)
mainWindow.mainloop()








