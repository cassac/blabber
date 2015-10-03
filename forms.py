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

    ## Future implementation: App needs to be modularized in order
    ## for below validation to function correctly. Currently
    ## there exists a circular import error when importing User
    ## object from models.py. For now, will use page reload and
    ## flash messages to notify user if username/email already registered

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #     self.user = None

    # def validate(self):
    #     rv = Form.validate(self)
    #     if not rv:
    #         return False

    #     username = User.query.filter_by(
    #         username=self.username.data).first()
    #     email = User.query.filter_by(
    #     	email=self.email.data).first()

    #     if username != None:
    #     	self.username.errors.append('Username already taken')
    #     	return False
    #     if email != None:
    #     	self.email.errors.append('Email address already registered')
    #     	return False

    #     if username == None and email == None:
    #     	return True  
