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


	