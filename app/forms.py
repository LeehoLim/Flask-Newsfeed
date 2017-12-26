from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

#Login Form including username, password, remember me, and submit fields
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

#Registration form including username, email, password
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	fname = StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	repeat_pw = PasswordField('Repeat Password', validators=[DataRequired()])
	submit = SubmitField('Create Account')

	#Method to validate and check whether the username exists or not
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already exists. Please select another username')

	#Method to validate whether or not the email is already registered with an account
	def validate_email(self, email):
		account = User.query.filter_by(email=email.data).first()
		if account is not None:
			raise ValidationError('Email is already registered with an account. Please login')

#Can make edits to your profile descriptiong or username
class EditProfile(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About Me', validators=[Length(min=0, max=256)])
	fname = StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	submit = SubmitField('Submit')


	def __init__(self, original_username, *args, **kwargs):
		super(EditProfile, self).__init__(*args, **kwargs)
		self.original_username = original_username
	

	#Have to double check that the username does not already exist
	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please choose a different username')

#Form to make a post
class PostForm(FlaskForm):
	post = TextAreaField('Send a message', validators=[DataRequired()])
	submit = SubmitField('Submit')

