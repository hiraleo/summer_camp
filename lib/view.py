from functools import wraps
from flask import request, redirect, url_for, render_template, flash, abort, jsonify, session, g
from lib import app, db
from lib.models import User, HyperLapse


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    g.user = session.get('id')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    target_user = User.query.filter(User.name == name).first()
    if target_user == None:
        return render_template('index.html', message="Your account not found")

    elif target_user.password == password:
        session['id'] = target_user.id
        session['user'] = name
        return redirect('/top')
    else:
        redirect('/')

@app.route('/register', methods=['GET'])
def regist_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def regist_user():
    name = request.form['name']
    if User.query.filter(User.name == name).first():
        return render_template('register.thml', message='username already exist')
    if request.form['password'] == request.form['passwd_confirmation']:
        password = request.form['password']
    user = User(
        name=name,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return index()

@app.route('/top', methods=['GET'])
@login_required
def top():
    late_project = HyperLapse.query.order_by(HyperLapse.created_at.desc())[:5]
    popular_project = HyperLapse.query.order_by(HyperLapse.fav.desc())[:5]
    context = {'latest': late_project, 'popular': popular_project}
    print(context['latest'])
    return render_template('top.html', latest=late_project, popular=popular_project)

@app.route('/logout')
@login_required
def logout():
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('index'))

@app.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    user_project = HyperLapse.query.filter(HyperLapse.creator == session['id'])
    return render_template('user.html', context=user_project)
