from flask import Flask, render_template, redirect, url_for, request, Response, g
from flask_login import LoginManager, UserMixin, login_required
import sqlite3
import models as db_handler

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

DATABASE = 'database.db'


class User():
    def __init__(self, name, email, password, active=True):
        self.name = name
        self.email = email
        self.password = password
        self.active = active

    @staticmethod
    def is_authenticated():
        return True
        # return true if user is authenticated, provided credentials

    @staticmethod
    def is_active():
        return True
        # return true if user is activte and authenticated

    def is_annonymous():
        return False
        # return true if annon, actual user return false

    def get_id():
        return unicode(self.id)
        # return unicode id for user, and used to load user from user_loader callback

    def __repr__(self):
        return '<User %r>' % (self.email)

    def add(self):
        db_handler.insert_user(self.username, self.password)


@login_manager.user_loader
def load_user(user_id):
    return db_handler.load_user(user_id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")  # naive token
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                return user
    return None


@app.route('/', methods=['POST', 'GET'])
def home():
    form = Login()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == db_handler.get_password(username):
            users = db_handler.retrieve_users()
            return render_template('LoginForm.html', users=users)
        else:
            return render_template('LoginForm.html', users='wrong')
    else:
        return render_template('LoginForm.html')


@app.route("/protected/", methods=["GET"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
app.run(port=5000, debug=True)
