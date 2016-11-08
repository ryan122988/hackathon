# -----------------------------------------------------------------------------
#
# This file is the copyrighted property of Tableau Software and is protected
# by registered patents and other applicable U.S. and international laws and
# regulations.
#
# Unlicensed use of the contents of this file is prohibited. Please refer to
# the NOTICES.txt file for further details.
#
# -----------------------------------------------------------------------------
import csv
import os
import types

from datetime import datetime
import sys
from tableausdk import *
from tableausdk.Extract import *
from tableausdk.Server import *

def isDateValid(dDate):
	try:
		validDate = datetime.strptime(dDate, '%b %d %Y %I:%M%p')
		return True
	except:
		return False
def isInt(nInt):
	try:
		validate = int(nInt)
		return validate == nInt
	except:
		return False
def isFloat(fFloat):
	try:
		
		validate = float(fFloat)
		return True
	except:
		return False
def isUnicode(sString):
	try:
		validate = str(sString, 'utf-8')
		return validate == sString
	except:
		return False

# Define the table's schema
def makeTableDefinition(headers, fileRow):
	tableDef = TableDefinition()
	tableDef.setDefaultCollation(Collation.EN_GB)
	
	if len(fileRow) != len(headers):
		# validate column count matches header length
		raise ValueError('Row (' + str(iRow) + ') element count does not match the header definition')
	for colIndex in range(len(fileRow)):
		headerName = headers[colIndex]
		column = fileRow[colIndex]
		if isInt(column):
			tableDef.addColumn(headerName, Type.INTEGER)
			print('Adding ' + headerName + ' as INTEGER')
		elif isFloat(column):
			tableDef.addColumn(headerName, Type.DOUBLE)
			print('Adding ' + headerName + ' as DOUBLE')
		elif isDateValid(column):
			tableDef.addColumn(headerName, Type.DATETIME)
			print('Adding ' + headerName + ' as DATETIME')
		elif isUnicode(column):
			tableDef.addColumn(headerName, Type.UNICODE_STRING)
			print('Adding ' + headerName + ' as UNICODE_STRING')
		else:
			tableDef.addColumn(headerName, Type.CHAR_STRING)
			print('Adding ' + headerName + ' as CHAR_STRING')
	return tableDef

# def printTableDefinition(tableDef):
	# print(tableDef.getColumnCount())
	# for i in range(tableDef.getColumnCount()):
		# type = tableDef.getColumnType(i)
		# name = tableDef.getColumnName(i)

		# sLine = 'Column ' + str(i) +'- ' + name + ' - '
		# if type == Type.INTEGER:
			# sLine += 'INTEGER'
		# elif type == Type.DOUBLE:
			# sLine += 'DOUBLE'
		# elif type == Type.DATETIME:
			# sLine += 'DATETIME'
		# elif type == Type.UNICODE_STRING:
			# sLine += 'UNICODE_STRING'
		# elif type == Type.CHAR_STRING:
			# sLine += 'CHAR_STRING'
			
        # print(sLine)

def printTableDefinition(tableDef):
	for i in range(tableDef.getColumnCount()):
		type = tableDef.getColumnType(i)
		name = tableDef.getColumnName(i)
	print >> sys.stderr, "Column {0}: {1} ({2:#06x})".format(i, name, type)

def insertData(table, fileRow):
	tableDef = table.getTableDefinition()
	
	print('Adding new row: ' + str(fileRow))
	row = Row(tableDef)
	for colIndex in range(len(fileRow)):
		expectedType = tableDef.getColumnType(colIndex)
		colVal = fileRow[colIndex]
		if expectedType == Type.INTEGER:
			print('Adding ' + str(colVal) + ' as INTEGER')
			if not isInt(colVal):
				raise ValueError(str(colVal) + ' cannot be case to INTEGER')
			row.setInteger(colIndex, int(colVal))
		elif expectedType == Type.DOUBLE:
			print('Adding ' + str(colVal) + ' as DOUBLE')
			if not isFloat(colVal):
				raise ValueError(str(colVal) + ' cannot be case to DOUBLE')
			row.setDouble(colIndex, float(colVal))
		elif expectedType == Type.DATETIME:
			print('Adding ' + str(colVal) + ' as DATETIME')
			row.setDateTime(colIndex, colVal)
		elif expectedType == Type.UNICODE_STRING:
			print('Adding ' + str(colVal) + ' as UNICODE_STRING')
			row.setString(colIndex, str(colVal, 'utf-8'))
		elif expectedType == Type.CHAR_STRING:
			print('Adding ' + str(colVal) + ' as CHAR_STRING')
			row.setCharString(colIndex, colVal)
	table.insert(row)

def publishCsvDatasource(serverURL, siteName, username, password, filename):

	extractName = os.path.basename(filename).split('.',2)[0]
	extractFilename = extractName + '.tde'
	try:
		os.remove(extractFilename)
	except OSError:
		pass
		
	ExtractAPI.initialize()
	with Extract(extractFilename) as extract:
		with open(filename) as csvfile:
			fileReader = csv.reader(csvfile, delimiter = ',')
			headers = []
			table = None
			for fileRow in fileReader:
				print('Reading: ' + str(fileRow))
				if headers == []:
					headers = fileRow
				else:
					if table == None:
						tableDef = makeTableDefinition(headers, fileRow)
						table = extract.addTable('Extract', tableDef)
					insertData(table, fileRow)
			csvfile.close()
		extract.close()
	ExtractAPI.cleanup()

	# Initialize Tableau Server API
	ServerAPI.initialize()
	serverConnection = ServerConnection()
	serverConnection.connect(serverURL, username, password, siteName);

	# Publish order-py.tde to the server under the default project with name Order-py
	serverConnection.publishExtract(extractFilename, 'default', extractName, False);
	

	# Disconnect from the server
	serverConnection.disconnect();

	# Destroy the server connection object
	serverConnection.close();

	# Clean up Tableau Server API
	ServerAPI.cleanup();
	
#publishCsvDatasource('https://na2-maxtst.zilliant.com/', 'customersupport4', 'mgreenslet', 'Z1ll1ant', 'orders.csv')

def main(argv):
	publishCsvDatasource(argv[1], argv[2], argv[3], argv[4], argv[5])

if __name__ == "__main__":
   main(sys.argv[1:])
