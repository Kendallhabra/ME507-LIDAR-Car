# Plot Python File

'''
Plot
This file opens, parses, and prints a CSV file.
Requirements:
	CSV File
		Exactly 2 columns
		Seperated by CSV
		May be whitespace
		Contains ints and floats
	Reject bad lines (print warning message)
	Graph
		Must be autoscaled
		Horizontal and vertical axis labels
		Axis labels must be SFW Python references/puns
	File must be named searing.py
	Cite all borrowed code
	Submit by emailing code as an attachment to me@me.me.calpoly.edu
	Must include proper comments and docstrings

'''

import matplotlib.pyplot as plt

# Plot constants
plotSettings = {
	"labelX": "*INSERT LABEL*",
	"labelY": "*INSERT LABEL*",
	}

filename = "data.csv"

def openCSV(filename):
	content = []
	with open(filename) as f:
		content = f.readlines()

	if len(content) == 0:
		print("ERROR: No data in file: ", filename)

	return content

def parseData(rawData):
	data = [[], []]
	for lineNum, line in enumerate(rawData):
		rawVals = line.split(",")
		
		if len(rawVals) != 2:
			lineWarning(lineNum, line, "does not contain 2 values")
			continue
		
		try:
			vals = [float(rawVals[0]), float(rawVals[1])]
		except ValueError:
			lineWarning(lineNum, line, "does not contain 2 valid numbers")
		else:
			data[0].append(vals[0])
			data[1].append(vals[1])

	return data

def buildPlot(data, plotSettings):
	plt.plot(data[0], data[1])

	plt.xlabel(plotSettings.get("labelX", "No Label"))
	plt.ylabel(plotSettings.get("labelY", "No Label"))
	plt.title(plotSettings.get("Title", "No Title"))
	plt.grid(True)
	plt.show()

def lineWarning(lineNum, line, error):
	print("WARNING: Line ", lineNum, ": \"", line[:-1], "\" ", error, ".", sep='')

rawData = openCSV(filename)
data = parseData(rawData)
buildPlot(data, plotSettings)




