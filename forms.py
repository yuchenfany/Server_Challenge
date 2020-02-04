from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired(), Length(min = 2, max = 20)])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class PostClub(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = TextAreaField('Description')
	tags = StringField('Tags')
	submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
	description = TextAreaField('Description')
	tags = StringField('Tags')
	submit = SubmitField('Submit')

class FavoriteForm(FlaskForm):
	clubname = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Favorite')