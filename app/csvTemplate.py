import csv
import os
import xml.etree.ElementTree as ET
import sys

#This function reads in and processes the csv input file
def readInCSV(filename):
	output = []
	with open(filename, newline='') as csvfile:
		fileReader = csv.reader(csvfile, delimiter = ',')
		for row in fileReader:
			output.append(row)
	return output

#Loops through the rows of input from the csv file sending for each row to be processed.  This function writes the output xml tree when processing completes	
def replaceValues(inputFileName, outputFileName, inputArray):
	tree = ET.parse(inputFileName)
	for row in inputArray:
		replaceValuesHelper(tree, row[0], row[1])
		
	tree.write(outputFileName)

#This is the helper function that replaces values for each individual row of input from the csv file	
def replaceValuesHelper(tree, configurationColumn, value):
	formula = isFormula(value)
	print(formula)
	actualValue = ''
	if formula == True:
		#actualValue = replaceSpecialCharacters(value)
		#actualValue = replaceFieldNamesWithActualValue(tree, actualValue)
		actualValue = replaceFieldNamesWithActualValue(tree, value)
	else: 
		actualValue = findReplacementValue(tree, value)
		actualValue = actualValue.replace('[', '')
		actualValue = actualValue.replace(']', '')
	root = tree.getroot()
	count = 0
	for column in root.iter('column'):
		try:
			if formula == False:
				if (str(column.attrib['caption'])) == configurationColumn:
					column.find("calculation").set('formula', '['+actualValue+']')
			else:
				if (str(column.attrib['caption'])) == configurationColumn:
					column.find("calculation").set('formula', actualValue)
		except:
			count += 1

#In the case that the value being put in from the template is a calculated attribute you must put the name tag much match the caption.  This method finds the name tag and calls recursively in case this field is also calculated			
def findReplacementValue(tree, value):
	root = tree.getroot()
	count = 0
	newValue = '-1'
	for column in root.iter('column'):
		try:
			if(str(column.attrib['caption'])) == value:
				newValue = str(column.get("name"))
		except:
			count += 1
			
	if newValue != '-1':
		testValue = findReplacementValue(tree, newValue)
		if testValue == newValue:
			return newValue
		else:
			return testValue
	else:
		return value
		
	return value
	
	
	

#function not necessary.  Tableau does this replacement automatically	
def replaceSpecialCharacters(s):
	replacedValues = []
	for char in s:
		if char == "'":
			replacedValues.append('&apos;')
		elif char == '"':
			replacedValues.append('&quot;')
		elif char == '>':
			replacedValues.append('&gt;')
		elif char == '<':
			replacedValues.append('&lt;')
		else:
			replacedValues.append(char)
	output = ''
	for val in replacedValues:
		output += val
	return output
	
#This formula does replacement of field names for formulas	
def replaceFieldNamesWithActualValue(tree, inputValue):
	chars = []
	temp = []
	open = False
	for char in inputValue:
		if char == '[':
			open = True
		elif char == ']':
			open = False
			str = ''
			for val in temp:
				str += val
			temp = []
			str = findReplacementValue(tree, str)
			str = str.replace('[', '')
			str = str.replace(']', '')
			str = '[' + str + ']'
			chars.append(str)
		elif open == True:
			temp.append(char)
		else:
			chars.append(char)
	output = ''
	for row in chars:
		output += row
	print (output)
	return output
	

def isFormula(str):
	formula = False
	if "[" in str:
		formula = True
	elif "(" in str:
		formula = True
	elif ">" in str:
		formula = True
	elif "<" in str:
		formula = True
	elif '"' in str:
		formula = True
	elif "'" in str:
		formula = True
	elif "*" in str:
		formula = True
	elif "/" in str:
		formula = True
	else:	
		return formula
	return formula

#Beginning of main code

#Read in CSV input file
#output = readInCSV(csvFile)

#Replace the values in the twb with the values found in the CSV
#replaceValues(inputFile, outputFile, output)