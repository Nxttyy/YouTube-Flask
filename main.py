from flask import Flask, render_template, redirect
from forms import SignupForm, LoginForm, VideoUploadForm
from flask_bcrypt import Bcrypt
import secrets, os
from models import User, Video, app, db


bcrypt = Bcrypt(app)

#variables to be improved(TEMP)
authenticated = False
authenticated_user_id = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global authenticated, authenticated_user_id
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            authenticated = True
            authenticated_user_id = user.id
            print('logged in')
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
        return redirect('/')
    return render_template('signup.html', form=form)

def savevideo(formfile):
    random_hex = secrets.token_hex(6)
    _, ext = os.path.splitext(formfile.filename)
    video_filename = random_hex + ext
    video_path = os.path.join((app.root_path), 'static/videos/', video_filename)
    formfile.save(video_path)
    return video_path

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if authenticated:
        form = VideoUploadForm()
        if form.validate_on_submit() and form.video.data:
            path = savevideo(form.video.data)
            vid = Video(caption=form.caption.data, file_path=path, user_id=authenticated_user_id)
            db.session.add(vid)
            db.session.commit()
            return redirect('/')
        return render_template('upload_video.html', form=form)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run()