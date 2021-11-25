######################################################################
#  PURPOSE: This contains key forms relevant for the "users" package #
######################################################################

from flask_wtf import FlaskForm #FlaskForm object contains the standard configuration needed for Flask-WTForms
from wtforms import StringField, PasswordField, SubmitField, BooleanField   #form Field objects (valid form input types)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError    #validator objects that check for valid form input
from flask_login import current_user #allows Forms to access the current_user User object
from TestTracker.models import User #imports the User class defined in models.py in the TestTracker package

#Inherits from FlaskForm
class RegistrationForm(FlaskForm):
    #Creates field objects
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators = [DataRequired(), Email()])
    password = PasswordField('Password',validators = [DataRequired()])
    confirmPassword = PasswordField('Confirm Password',validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register!')

    #------------------------------------
    #Flask will run the following validation method checks on it's own upon attempting to submit the form, without an explicit method call:
    #-------------------------------------
    #EXTRA VALIDATOR #1: Checks whether username already exists in the database
    #PARAM: String username (inputted into this form)
    #RAISES: Exception called ValidationError if another User has already claimed that username
        #else raises nothing
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #searches database for User with the form input's username
        if user:
            raise ValidationError('This username is already taken ... Choose another.')

    #EXTRA VALIDATOR #2: Checks whether email already exists in the database
    #PARAM: String email (inputted into this form)
    #RAISES: Exception called ValidationError if another User has already claimed that email
        #else raises nothing
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #searches database for User with the form input's email
        if user:
            raise ValidationError('This email is already taken ... Choose another.')

#Inherits from FlaskForm
class LoginForm(FlaskForm):
    #Creates form field objects
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me?')
    submit = SubmitField('Login!')

#Inherits from FlaskForm
class UpdateAccountForm(FlaskForm):
    #Creates form field objects
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Update!')

    #------------------------------------
    #Flask will run the following validation method checks on it's own upon attempting to submit the form, without an explicit method call:
    #-------------------------------------
    #EXTRA VALIDATOR #1: Checks whether username already exists in the database
    #PARAM: String username (inputted into this form)
    #RAISES: Exception called ValidationError if a DIFFERENT User has already claimed that username (you can keep your old username)
        #else raises nothing
    def validate_username(self, username):
        #This conditional allows you to keep the same username
        #It will only search through the database if you try to change your username to something else
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken ... Choose another.')

    #EXTRA VALIDATOR #2: Checks whether email already exists in the database
    #PARAM: String email (inputted into this form)
    #RAISES: Exception called ValidationError if a DIFFERENT User has already claimed that email (you can keep your old email)
        #else raises nothing
    def validate_email(self, email):
        #This conditional allows you to keep the same email
        #It will only search through the database if you try to change your email to something else
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken ... Choose another.')
