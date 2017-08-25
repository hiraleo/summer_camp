from flask import request, redirect, url_for, render_template, flash, session
from lib import app, db
from lib.models import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    target_user = User.query.filter(User.name == name).first()
    if target_user.password == password:
        session['id', 'name'] = [target_user.id, name]
        return redirect('/top')

