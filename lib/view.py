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


@app.route('/user/<user_name>')
@login_required
def user_detail(user_name):
    user_project = HyperLapse.query.filter(HyperLapse.creator == user_name)
    return render_template('user.html', context=user_project)


@app.route('/search')
@login_required
def keyword():
    keyword = '%{keyword}%'.format(keyword=request.args.get('search'))
    print(keyword)
    user_project = HyperLapse.query.filter(HyperLapse.name.like(keyword)).all()
    print(user_project)
    return render_template('result.html', context=user_project)


@app.route('/project')
@login_required
def create_project():
    default_project = HyperLapse.query.filter(HyperLapse.id == 4).all()[0]
    print(default_project)
    return render_template('viewer.html', project=default_project)


@app.route('/project/save', methods=['POST'])
@login_required
def save_project():
    json = request.json
    print(json)
    hyperlapse = HyperLapse(
        name=json['name'],
        start_latlng1=json['startPoint1'],
        start_latlng2=json['startPoint2'],
        end_latlng1=json['endPoint1'],
        end_latlng2=json['endPoint2'],
        viewpoint_latlng1=json['lookatPoint1'],
        viewpoint_latlng2=json['lookatPoint2'],
        creator=session.get('user')
    )
    db.session.add(hyperlapse)
    db.session.commit()
    result = {
        'Result': {
            'text': "success"
        }
    }
    return jsonify(ResultSet=result)

@app.route('/favorite')
@login_required
def favb():
    fav +=request.json['fav'] 
    
@app.route('/project/<project_id>')
@login_required
def render_project(project_id):
    target_project = HyperLapse.query.filter(id == project_id).all()
    if(len(target_project) == 0):
        flash('project not found')
        return redirect(url_for('top'))
    else:
        return render_template('viewer.html', project=target_project)


