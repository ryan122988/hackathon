from flask import Flask, session, render_template, request, flash, url_for, redirect, abort, g, Response
#from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app


'''

@app.before_request
def before_request():
	g.user = current_user

'''


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

	if request.method == 'GET':

		return render_template('index.html', title='Home')


@app.route('/calculationReplacement', methods=['GET', 'POST'])
def calculationReplacement():

	if request.method == 'GET':

		return render_template('calculationReplacement.html', title='calculation replacement')


@app.route('/siteMigration', methods=['GET', 'POST'])
def siteMigration():

	if request.method == 'GET':

		return render_template('siteMigration.html', title='site migration')


		