from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.session import Session

app = Flask(__name__, template_folder='../src/template', static_folder='../src')
app.config.from_object('lib.config')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

import lib.view
