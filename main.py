from flask import Flask, render_template, redirect, session, abort
from forms import SignupForm, LoginForm, VideoUploadForm, CommentForm
from flask_bcrypt import Bcrypt
import secrets, os
from models import User, Video, Comment, app, db


bcrypt = Bcrypt(app)

@app.route('/')
def home():
    videos = Video.query.all()
    return render_template('home.html', videos = videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['logged_in'] = True
            session['user_id'] = user
            flash('logged in')
            return redirect('/')
        else:
            print('wrong password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_pass = (bcrypt.generate_password_hash(form.password.data)).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        session['user_id'] = user.id
        return redirect('/')
    return render_template('signup.html', form=form)

def savevideo(formfile):
    random_hex = secrets.token_hex(6)
    _, ext = os.path.splitext(formfile.filename)
    video_filename = random_hex + ext
    video_path = os.path.join((app.root_path), 'static/videos/', video_filename)
    formfile.save(video_path)
    return video_filename

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if session['logged_in']:
        form = VideoUploadForm()
        if form.validate_on_submit() and form.video.data:
            path = savevideo(form.video.data)
            vid = Video(caption=form.caption.data, file_path=path, user_id=session['user_id'])
            db.session.add(vid)
            db.session.commit()
            return redirect('/')
        return render_template('upload_video.html', form=form)
    else:
        return redirect('/')

@app.route("/video/<vid_id>", methods=['GET', 'POST'])
def video(vid_id):
    form=CommentForm()
    video = Video.query.get(vid_id)
    videos = Video.query.all()
    comments=Comment.query.all()
    if form.validate_on_submit() and form.content.data:
        comment = Comment(content=form.content.data, user_id=session['user_id'], video_id=vid_id)
        db.session.add(comment)
        db.session.commit()
        form.content.data = ''
    if video:
        return render_template('player.html', video=video, videos=videos, form=form, comments=comments)
    return abort(404)

# @app.route('/comment/<vid_id>', methods=['GET', 'POST'])
# def comment(vid_id):
#     form = CommentForm()
    
#     return redirect('video', vid_id=vid_id)
if __name__ == '__main__':
    app.run()