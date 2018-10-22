# create models
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='postauth', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.username)

class Followers(db.Model):
    __tablename__ = 'followers'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)

class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer, db.ForeignKey('users.uid') , nullable=False)
    content = db.Column(db.String(1024), nullable=False)
