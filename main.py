from flask import request, render_template, redirect, session, abort
from forms import SignupForm, LoginForm, VideoUploadForm, CommentForm, PlaylistForm
from flask_bcrypt import Bcrypt
import secrets, os
from models import User, Video, Comment, db, login, Playlist
from flask_login import login_required, current_user, login_user, logout_user
from app import app
from flask_bootstrap import Bootstrap


bcrypt = Bcrypt(app)
Bootstrap(app)

login.init_app(app)
login.login_view = 'login'


@app.route('/')
def home():
    videos = Video.query.all()
    return render_template('home.html', videos = videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect('/account')

    if request.method == 'POST':
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect('/account')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if current_user.is_authenticated:
        return redirect('/account')
     
    if request.method == 'POST':
        email = form.email.data
        username = form.username.data
        password = form.password.data
 
        if User.query.filter_by(username=username).first():
            return ('Email already Present')
        
        pass_hashed = bcrypt.generate_password_hash(request.form['password'])
        user = User(email=email, username=username, password=pass_hashed)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


def savevideo(formfile):
    random_hex = secrets.token_hex(6)
    _, ext = os.path.splitext(formfile.filename)
    video_filename = random_hex + ext
    video_path = os.path.join((app.root_path), 'static/videos/', video_filename)
    formfile.save(video_path)
    return video_filename

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if current_user.is_authenticated:
        form = VideoUploadForm()
        if form.validate_on_submit() and form.video.data:
            path = savevideo(form.video.data)
            vid = Video(caption=form.caption.data, file_path=path, user_id=current_user.id)
            db.session.add(vid)
            db.session.commit()
            return redirect('/')
        return render_template('upload_video.html', form=form)
    else:
        return redirect('login')

@app.route("/video/<vid_id>", methods=['GET', 'POST'])
def video(vid_id):
    form=CommentForm()
    video = Video.query.get(vid_id)
    videos = Video.query.all()
    comments=Comment.query.filter_by(video_id=vid_id)
    if form.validate_on_submit() and form.content.data:
        comment = Comment(content=form.content.data, user_id=session['user_id'], video_id=vid_id)
        db.session.add(comment)
        db.session.commit()
        form.content.data = ''
    if video:
        return render_template('player.html', video=video, videos=videos, form=form, comments=comments)
    return abort(404)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
        user = current_user
        return render_template('account.html', user=user)
    return redirect('/signup')

@app.route('/playlist', methods=['GET', 'POST'])
@login_required
def playlist():
    playlists = Playlist.query.all()
    form = PlaylistForm()
    if request.method == 'POST':
        playlist = Playlist(title=form.title.data, private=form.private.data, user_id = current_user.id)
        db.session.add(playlist)
        db.session.commit()
        playlists = Playlist.query.all()
    
    return render_template('playlist.html', form=form, playlists=playlists)
if __name__ == '__main__':
    app.run()