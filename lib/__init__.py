from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.session import Session

app = Flask(__name__, template_folder='../src/template')
app.config.from_object('lib.config')

db = SQLAlchemy(app)
SESSION_TYPE = 'redis'
Session(app)

import lib.view
