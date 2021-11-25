######################################################################
#  PURPOSE: This contains key forms relevant for the "tests" package #
######################################################################

from flask_wtf import FlaskForm #FlaskForm object contains the standard configuration needed for Flask-WTForms
from wtforms import StringField, SubmitField, IntegerField  #form Field objects (specify valid form input types)
from wtforms.validators import DataRequired, NumberRange, ValidationError   #validator objects that check for valid form input

#Inherits from FlaskForm
class ACTForm(FlaskForm):
    #Creates form field objects
    english = IntegerField('English',validators=[DataRequired(message='Please enter an integer from 1 to 36'),NumberRange(min=1,max=36)])
    math = IntegerField('Math',validators=[DataRequired(message='Please enter an integer from 1 to 36'),NumberRange(min=1,max=36)])
    reading = IntegerField('Reading',validators=[DataRequired(message='Please enter an integer from 1 to 36'),NumberRange(min=1,max=36)])
    science = IntegerField('Science',validators=[DataRequired(message='Please enter an integer from 1 to 36'),NumberRange(min=1,max=36)])
    submit = SubmitField('Save!')

#Inherits from FlaskForm
class SATForm(FlaskForm):
    #Creates form field objects
    ebrw = IntegerField('EBRW',validators=[DataRequired(message='Please enter an integer from 200 to 800'),NumberRange(min=200,max=800)])
    math = IntegerField('Math',validators=[DataRequired(message='Please enter an integer from 200 to 800'),NumberRange(min=200,max=800)])
    submit = SubmitField('Save!')

    #------------------------------------
    #Flask will run the following validation method checks on it's own upon attempting to submit the form, without an explicit method call:
    #-------------------------------------
    #EXTRA VALIDATION #1 -- Checks whether ebrw score is a multiple of 10, as per CollegeBoard SAT/PSAT guidelines
    #PARAM: int ebrw section score
    #RAISES: Exception called ValidationError if the ebrw score is not a multiple of 10, as per CollegeBoard SAT/PSAT guidelines.
            #else raises nothing
    def validate_ebrw(self,ebrw):
        if ebrw.data % 10 != 0:
            raise ValidationError('Scores should be a multiple of 10. Please enter a valid score.')

    #EXTRA VALIDATION #2 -- Checks whether math score is a multiple of 10, as per CollegeBoard SAT/PSAT guidelines
    #PARAM: int math section score
    #RAISES: Exception called ValidationError if the math score is not a multiple of 10, as per CollegeBoard SAT/PSAT guidelines.
            #else raises nothing
    def validate_math(self,math):
        if math.data % 10 != 0:
            raise ValidationError('Scores should be a multiple of 10. Please enter a valid score.')

#Inherits from SATForm -- including the validate_ebrw(self, ebrw) and validate_math(self, math)
class PSATForm(SATForm):
    #Creates form field objects
    ebrw = IntegerField('EBRW',validators=[DataRequired(message='Please enter an integer from 200 to 760'),NumberRange(min=200,max=760)])
    math = IntegerField('Math',validators=[DataRequired(message='Please enter an integer from 200 to 760'),NumberRange(min=200,max=760)])
    submit = SubmitField('Save!')
