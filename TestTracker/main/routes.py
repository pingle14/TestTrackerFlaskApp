##################################################################################
#  PURPOSE: This file contains all the routes relevant to the "main" Blueprint   #
##################################################################################

from flask import render_template, Blueprint

main = Blueprint("main", __name__)  #instantiates a Blueprint object called "main"

#This @Blueprint_name.route decorator adds Link/route functionality to the method

#RETURNS: A response to render the about.html template
@main.route('/')
@main.route('/about')
def about():
    return render_template('about.html', title='About')
