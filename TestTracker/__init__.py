#########################################################################################
#  PURPOSE: This file is where I initialize the application & integrate key components  #
#########################################################################################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#CONFIGURATION OF NECESSARY GLOBAL VARS

app = Flask(__name__) #instantiates the Flask class as my WSGI application ..
#   ...WSGI = Web Server Gateway Interface = calling convention for web servers to forward requests to Python web applications/frameworks

app.config['SECRET_KEY'] = '8d6033e675b5050aa03f65f7b9e83aa0' #secret key - protect against modifying cookies & cross-site request forgery attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  #saves the database on my file system in this project as "site.db"
db = SQLAlchemy(app)    #instantiates SQL Database
bcrypt = Bcrypt(app)    #instantiates the object that hashes and checks passwords
login_manager = LoginManager(app)   #instantiates the object that manages login sessions.
#   ...This adds functionality to db models so it will handle the sessions in the background for me

login_manager.login_view = 'users.login'  #passed in blueprint.function_name
login_manager.login_message_category = 'warning' #any weird login-related messages will be formatted as bootstrap-warning


#Import from files in this TestTracker package at end to avoid circular imports
from TestTracker.users.routes import users  #users = Blueprint instance
from TestTracker.tests.routes import tests  #tests = Blueprint instance
from TestTracker.main.routes import main  #main = Blueprint instance
from TestTracker.errors.handlers import errors  #errors = Blueprint instance
app.register_blueprint(users)   #registers the users Blueprint to the application
app.register_blueprint(tests)   #registers the tests Blueprint to the application
app.register_blueprint(main)   #registers the main Blueprint to the application
app.register_blueprint(errors)   #registers the errors Blueprint to the application
