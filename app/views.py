from flask import Flask, session, render_template, request, flash, url_for, redirect, abort, g, Response, send_from_directory
#from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, csvTemplate
import logging, logging.handlers

import os
from werkzeug import secure_filename
'''

@app.before_request
def before_request():
	g.user = current_user

'''
ALLOWED_EXTENSIONS = set(['tde', 'twb', 'csv'])

def allowed_file(filename):
	return'.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

	if request.method == 'GET':

		return render_template('index.html', title='Home')


	server = request.form['server']
	site = request.form['site']
	username = request.form['username']
	password = request.form['password']


	files = request.files.getlist("file[]")
	print(files)
	#file = request.files['file']
	csvFile = ''
	tableauFile = ''
	outputFileWithPath = ''
	outputFile = ''
	for file in files:
		logging.error(file.filename)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if file.filename.rsplit('.', 1)[1] == 'csv':
				csvFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			else:
				tableauFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				outputFileWithPath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
				outputFile = filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#print (filename)

	logging.error(csvFile)
	logging.error(server)
	#createExtract.publishCsvDatasource(server, site, username, password, csvFile)
	#os.system("python "+server+" "+site+" "+username+" "+password+" "+csvFile)
	return render_template('success.html', title='Success')
		

@app.route('/calculationReplacement', methods=['GET', 'POST'])
def calculationReplacement():

	if request.method == 'GET':

		return render_template('calculationReplacement.html', title='calculation replacement')


	files = request.files.getlist("file[]")
	
	#file = request.files['file']
	csvFile = ''
	tableauFile = ''
	outputFileWithPath = ''
	outputFile = ''
	for file in files:
		logging.error(file.filename)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if file.filename.rsplit('.', 1)[1] == 'csv':
				csvFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			else:
				tableauFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				outputFileWithPath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
				outputFile = filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#print (filename)
		
	#call to csvTemplate to read in the csv file
	output = csvTemplate.readInCSV(csvFile)
	#ouptutFIle = '\\downloads\\ouput.twb'
	csvTemplate.replaceValues(tableauFile, outputFileWithPath, output)
	if os.path.isfile(csvFile):
		os.remove(csvFile)
	if os.path.isfile(tableauFile):
		os.remove(tableauFile)
	return redirect(url_for('uploaded_file', filename=outputFile))




@app.route('/downloads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)
	


@app.route('/siteMigration', methods=['GET', 'POST'])
def siteMigration():

	if request.method == 'GET':

		return render_template('siteMigration.html', title='site migration')


'''
@app.route('/publish', methods=['GET', 'POST'])
def publish():

	if request.method == 'GET':

		return render_template('publish.html', title='publish')

'''
		