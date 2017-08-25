from flask import request, redirect, url_for, render_template, flash
from lib import app, db
from lib.models import User


@app.route('/')
def show_login():
    return render_template('index.html')
