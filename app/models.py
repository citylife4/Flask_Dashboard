from appdirs import unicode

from app import db, bcrypt

from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

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

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def check_password(self, password):
        # return check_password_hash(self.password, password)
        return bcrypt.check_password_hash(self.password, password)

    # Todo : add possibility to admins to create and delete users on site

    def __repr__(self):
        return '<User %r>' % self.username


