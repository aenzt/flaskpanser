from enum import unique
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
import datetime
from flask.helpers import make_response
from flask_login.utils import login_required
from flask_security.datastore import SQLAlchemyUserDatastore
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemySessionUserDatastore, LoginForm, login_required, login_user, UserMixin, RoleMixin
from sqlalchemy.sql.schema import ForeignKey
from flask_security.utils import hash_password, logout_user
from wtforms import StringField
from wtforms.validators import InputRequired
from Adafruit_IO import Client

app = Flask(__name__)
app.config['SECRET_KEY']= '5RandomStrings'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ghazial06@localhost/flaskapp'
app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ('username','email')

aio = Client('raihanpl', 'aio_hGHF14BX49K1gThdYqcX5eoCjFrq')

db = SQLAlchemy(app)

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer, db.ForeignKey('user.id')), db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

#TODO : Make API Connect with adafruit
#TODO : Make jquery no refresh thingy
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role', 
        secondary=roles_users, 
        backref=db.backref('users', lazy='dynamic')
    )


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

class ExtendeLoginForm(LoginForm):
    email = StringField('Username or Email Address', [InputRequired()])

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form = ExtendeLoginForm)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        user_datastore.create_user(
            email = request.form.get('email'),
            username = request.form.get('username'),
            name = request.form.get('name'),
            password = hash_password(request.form.get('password'))
        )
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('index.html')

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method =='POST':
#         user_datastore.create_user(
#             email = request.form.get('email'),
#             password = hash_password(request.form.get('password'))
#         )
#         db.session.commit()
        
#         return redirect(url_for('profile'))
#     return render_template('register.html')
    
@app.route('/login', methods =['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(User)

        flash ('Logged In Succesfully')
        
        return redirect(url_for('dashboard'))
    
    return redirect (url_for('dashboard'), form = form)

@app.route('/dashboard')
@login_required
def dashboard ():
    # url_servo = 'https://io.adafruit.com/api/v2/raihanpl/feeds/servo/data'
    # url_photocell = 'https://io.adafruit.com/api/v2/raihanpl/feeds/photocell/data'
    
    return render_template ('dashboard.html')

@app.route('/post1', methods = ['POST', 'GET'])
def post():
    val1 = request.form['value1']
    # val2 = request.form['value2']
    # val3 = request.form['value3']

    print(val1)
    senddata = aio.feeds('servo')
    aio.send_data(senddata.key, int(val1))
    senddata1 = aio.feeds('servo1')
    # aio.send_data(senddata1.key, int(val2))
    # senddata2 = aio.feeds('servo2')
    # aio.send_data(senddata2.key, int(val3))

    res = make_response(jsonify({"message" : "OK"}), 200)

    return res

@app.route('/post2', methods = ['POST', 'GET'])
def post2():
    # val1 = request.form['value1']
    val2 = request.form['value2']
    # val3 = request.form['value3']

    # senddata = aio.feeds('servo')
    # aio.send_data(senddata.key, int(val1))
    senddata1 = aio.feeds('servo1')
    aio.send_data(senddata1.key, int(val2))
    # senddata2 = aio.feeds('servo2')
    # aio.send_data(senddata2.key, int(val3))

    res = make_response(jsonify({"message" : "OK"}), 200)

    return res

@app.route('/post3', methods = ['POST', 'GET'])
def post3():
    # val1 = request.form['value1']
    # val2 = request.form['value2']
    val3 = request.form['value3']

    # senddata = aio.feeds('servo')
    # aio.send_data(senddata.key, int(val1))
    # senddata1 = aio.feeds('servo1')
    # aio.send_data(senddata1.key, int(val2))
    senddata2 = aio.feeds('servo2')
    aio.send_data(senddata2.key, int(val3))

    res = make_response(jsonify({"message" : "OK"}), 200)

    return res

@app.route('/update')
def update ():
    r = aio.receive('servo')
    s = aio.receive('servo1')
    t = aio.receive('servo2')
    u = aio.receive('photocell')
    #feed = js_obj ['feed_key']
    servoval = int(r.value)
    servo1val = int(s.value)
    servo2val = int(t.value)
    photocellval = int(u.value)
    return jsonify(servoval=servoval,
                    servo1val=servo1val,
                    servo2val=servo2val,
                    photocellval=photocellval) 

@app.route('/logout')
@login_required
def logout():
    logout_user
    return redirect (url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)