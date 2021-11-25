#########################################################################################
#  PURPOSE: This file contains all the class definitions used in the SQL database       #
#########################################################################################

from datetime import datetime
from TestTracker import db, login_manager
from flask_login import UserMixin   #Required to make flask_login work correctly .. configures common variables

#Reloads the user from the current session by the user's id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Inherits from both db.Model and UserMixin
#This is the User class, which is stored in an SQLLite database for Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    #primary_key means this is a unique id for our user
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    #tests is not an actual column, but instead running an additional getter query to get all tests authored/created by the User
    #I used capital "T" for Test because I am referencing the class
    #"author" is the backreference that ties the Test to the User that created it
    tests = db.relationship('Test', backref='author', lazy=True)

    #toString method for User object
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#Inherits from db.Model
class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    report = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    #use lowercase "user" because ref table/column name, not the class

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':None #This ensures that Test possesses abstract class behavior ...
    }

    #toString method for Test object
    def __repr__(self):
        return f"Test('{self.type}', '{self.date_posted}', '{self.report}')"

    #to be implemented in the child classes: SAT, ACT
    def calculate_cummulative_score(self, scores_dict):
         pass

#Inherits from Test
class ACT(Test):
    __mapper_args__ = {'polymorphic_identity':'ACT'}

    #PARAM: scores_dict is a Pandas dataframe, which acts similar to a multidimensional HashMap
    #RETURNS: For ACT, cummulative score is a ROUNDED AVERAGE of all section scores
    def calculate_cummulative_score(self, scores_dict):
        return round(float(sum(scores_dict.values())) / len(scores_dict))

#Inherits from Test
class SAT(Test):
    __mapper_args__ = {'polymorphic_identity':'SAT'}

    #PARAM: scores_dict is a Pandas dataframe, which acts similar to a multidimensional HashMap
    #RETURNS: For SAT, cummulative score is a SUM of both section scores
    def calculate_cummulative_score(self, scores_dict):
        return sum(scores_dict.values())

#Inherits from SAT
class PSAT(SAT):
    __mapper_args__ = {'polymorphic_identity':'PSAT'}

    #PSAT class inherits the SAT calculate_cummulative_score(self, scores_dict)
