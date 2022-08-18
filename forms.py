from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class SignupForm(FlaskForm):
   username = StringField('username', [validators.DataRequired()])
   email = StringField('email', [validators.DataRequired(), validators.Email()] )
   password = PasswordField('password', [validators.DataRequired(), validators.EqualTo('confirm', message='password does not match.')])
   confirm = PasswordField('repeat password')
   submit = SubmitField('sign-up')

class LoginForm(FlaskForm):
   username = StringField('username', [validators.DataRequired()])
   password = PasswordField('password', [validators.DataRequired()])
   submit = SubmitField('login')
