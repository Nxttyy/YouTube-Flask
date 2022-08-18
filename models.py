from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.secret_key = 'f25e42871b71d695e0edb0deb4404fab'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    videos = db.relationship('Video', backref='user', lazy=True)

    def __repr__(self):
        return self.username

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(200), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
