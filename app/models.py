__author__ = 'cruor'
from app import db
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_PREMIUM = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    pwdhash = db.Column(db.String(120))
    created = db.Column(db.DATETIME)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self, username, password, email):
        self.nickname = username
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.role = ROLE_USER
        self.created = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)