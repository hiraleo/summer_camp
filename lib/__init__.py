from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../src/template')
app.config.from_object('lib.config')

db = SQLAlchemy(app)

import lib.view
