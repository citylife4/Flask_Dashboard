from app import app, login_manager, db
from .models import User
from forms import LoginForm

from flask import Flask, request, flash, url_for, redirect, render_template, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


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
    print(registered_user)
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    print("asd")
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
