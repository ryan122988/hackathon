from flask import Flask
#from flask_bootstrap import Bootstrap

import logging, logging.handlers
#from app import configuration
import os
#from werkzeug import secure_filename

#cwd = os.getcwd()
UPLOAD_FOLDER = 'C:\\temp\\hackathon\\upload'
DOWNLOAD_FOLDER = 'C:\\temp\\hackathon\\download'

#print(cwd)
#print(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

logging.basicConfig(filename='app.log', level=logging.INFO,format='%(asctime)s %(message)s')
logging.info('Started')
logging.info('finished')

from app import views