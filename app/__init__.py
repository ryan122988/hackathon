from flask import Flask
#from flask_bootstrap import Bootstrap

import logging, logging.handlers
#from app import configuration

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctim)s %(message)s')
logging.info('Started')
logging.info('finished')

from app import views