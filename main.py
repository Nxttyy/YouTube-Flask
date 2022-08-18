from flask import Flask, render_template, redirect
from forms import SignupForm, LoginForm
from flask_bcrypt import Bcrypt
#from flask_wtf import validate_on_submit
from models import User, app, db


bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
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

if __name__ == '__main__':
    app.run()