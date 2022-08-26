from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, BooleanField
from flask_wtf.file import FileField, FileRequired
from models import User

class SignupForm(FlaskForm):
   username = StringField('username', [validators.DataRequired()])
   email = StringField('email', [validators.DataRequired(), validators.Email()] )
   password = PasswordField('password', [validators.DataRequired(), validators.EqualTo('confirm', message='password does not match.')])
   confirm = PasswordField('repeat password')
   submit = SubmitField('sign-up') 

   def validate_username(form, username):
      username_taken = User.query.filter_by(username=username.data).first()
      if username_taken:
         raise ValidationError('Username is taken')

class LoginForm(FlaskForm):
   username = StringField('username', [validators.DataRequired()])
   password = PasswordField('password', [validators.DataRequired()])
   submit = SubmitField('login')

class VideoUploadForm(FlaskForm):
   caption = StringField('caption', [validators.DataRequired()])
   video = FileField(validators = [FileRequired()])
   submit = SubmitField('upload')

class CommentForm(FlaskForm):
   content=StringField('comment', [validators.DataRequired()])
   submit = SubmitField('post')

class PlaylistForm(FlaskForm):
   title=StringField('title', [validators.DataRequired()])
   private = BooleanField('private', false_values=(False, 'false', 0, '0')) 
   submit = SubmitField('post')
