from wtforms import Form, BooleanField, StringField, PasswordField, TextField, validators
import models as db_handler
from datetime import datetime
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
DATABASE = 'database.db'


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    #email = db.Column('email', db.String(50), unique=True, index=True)
    #registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()


    @property
    def is_authenticated(self):
        return True
        # return true if user is authenticated, provided credentials

    @property
    def is_active(self):
        return True
        # return true if user is activte and authenticated

    @property
    def is_annonymous(self):
        return False
        # return true if annon, actual user return false

    @property
    def get_id(self):
        return unicode(self.id)
        # return unicode id for user, and used to load user from user_loader callback

    def check_password(self, password):
        # return check_password_hash(self.password, password)
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username

    def add(self):
        db_handler.insert_user(self.username, self.password)


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('LoginForm.html', form=form)

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    print(registered_user)
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=5000, debug=True)
