from datetime import datetime
from flask_login import UserMixin, LoginManager
from app import app, db

login = LoginManager()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    profile_img = db.Column(db.String(12), nullable=False, default='default.jpg')
    videos = db.relationship('Video', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    playlists = db.relationship('Playlist', backref='user', lazy=True)


    def __repr__(self):
        return self.username

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(200), unique=False, nullable=False)
    file_path = db.Column(db.String(12), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    views = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='video', lazy=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dis_likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    videos = db.relationship('Video', backref='playlist', lazy=True)
    private = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

