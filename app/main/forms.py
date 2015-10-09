from flask_wtf import Form
from wtforms import (StringField, SubmitField, PasswordField,
    BooleanField)
from wtforms.validators import (DataRequired, Email, Length, 
	EqualTo, Required)

class LoginForm(Form):
    email = StringField('Email', 
        validators=[Email('Invalid Email Address')])
    password = PasswordField('Password',
        validators=[DataRequired('Enter Password')])
    remember_me = BooleanField('Keep me signed in', default=True)
    submit = SubmitField('Login')

class SignUpForm(Form):
    email = StringField('Email', 
		validators=[Email('Invalid Email Address'),
		DataRequired('Must provide email'),
		Length(max=50, message='Email address is too long')])
    username = StringField('Username', 
		validators=[Length(min=4, max=25, message='Username must be between\
			4 and 25 characters in length')])
    password = PasswordField('Password', 
		validators=[Required('Type in a password'), 
					EqualTo('confirm', message='Passwords must match'),
					Length(min=8, max=50, message='Password must be between 8 and\
						50 characters in length')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up!')
