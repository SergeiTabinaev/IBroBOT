import os

from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from IB import runIB
import sys
import logging


app = Flask(__name__)
app.config.from_object(Configuration)


####################################################

runIB() #ордер на покупку


####################################################

# logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'mylog.log')
## sys.stderr = open('log.txt', 'w')

######################################################

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

######################################################
