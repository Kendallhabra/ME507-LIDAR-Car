'''
Plot Python File

This file opens, parses, and plots the data in a CSV file.

The CSV file is selected with the -f flag or defaults to data.csv.

Written by Kendall Searing for ME507-01 Homework 0
2016-10-26
'''

import matplotlib.pyplot as plt
import argparse
from pathlib import Path
import re

# Global Constants
plotSettings = {
	"labelX": "*INSERT LABEL*",
	"labelY": "*INSERT LABEL*",
	"title": "*INSERT LABEL*",
	}

defaultFilename = "data.csv"

def main():
	"""Open, parse, and plot the data in a CSV file."""
	filename = getFilename(defaultFilename)
	if filename:
		rawData = openCSV(filename)
		data = parseData(rawData)
		buildPlot(data, plotSettings)


def getFilename(defaultFilename):
	"""Check and return the filename depending on the command line arguments."""
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filename', help = 'Name of the csv file to plot.', action = 'store')
	arguments = parser.parse_args()
	filename = arguments.filename or defaultFilename

	# Returns the filename or the default filename if they exist.
	if Path(filename).is_file():
		print("Opening data from: ", filename, sep='')
		return filename
	elif Path(defaultFilename).is_file():
		print("WARNING: ", filename, " could not be found.  Opening default file: ", defaultFilename, " instead.", sep='')
		return defaultFilename
	else:
		print("ERROR: ", filename, " could not be found.", sep='')
		return None


def openCSV(filename):
	"""Open a csv file and return the lines as a list of strings."""
	content = []
	with open(filename) as f:
		content = f.readlines()

	if len(content) == 0:
		print("ERROR: No data in file: ", filename, sep='')

	return content

def parseData(rawData):
	"""Open a csv file and return the lines as a list of strings."""
	data = [[], []]
	for lineNum, rawLine in enumerate(rawData):
		if len(rawLine) <= 1:
			lineWarning(lineNum, rawLine, "is empty")
			continue
				
		# Remove invalid characters from the line.
		strippedLine = re.sub(r"[\s]+", "", rawLine)
		line = re.sub(r"[^\d,.-]+", "", strippedLine)

		# Attempts to convert both values in the line into floating point numbers.
		rawVals = line.split(",")
		if len(rawVals) != 2:
			lineWarning(lineNum, rawLine, "does not contain 2 values")
			continue
		try:
			vals = [float(rawVals[0]), float(rawVals[1])]
		except ValueError:
			lineWarning(lineNum, rawLine, "does not contain 2 valid numbers")
			continue
		else:
			data[0].append(vals[0])
			data[1].append(vals[1])
		if line != strippedLine:
			lineWarning(lineNum, rawLine, "will be parsed as \"" + line + "\"")

	return data

def buildPlot(data, plotSettings):
	"""Build and show a plot based on the extracted data."""
	plt.plot(data[0], data[1])

	print("")
	plt.xlabel(plotSettings.get("labelX", "No Label"))
	plt.ylabel(plotSettings.get("labelY", "No Label"))
	plt.title(plotSettings.get("title", "No Title"))
	plt.grid(True)
	plt.show()

def lineWarning(lineNum, line, error):
	"""Print a warning message about a specific line."""
	print("WARNING: Line ", lineNum + 1, ": \"", line[:-1], "\" ", error, ".", sep='')

if __name__ == '__main__':
	main()




