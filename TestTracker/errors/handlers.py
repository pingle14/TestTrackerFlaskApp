#############################################################################################
#  PURPOSE: This file contains all the handler methods relevant to the "errors" Blueprint   #
#############################################################################################


from flask import Blueprint, render_template

errors = Blueprint("errors",__name__)   #instantiates a Blueprint object called "errors"

#Error handlers kinda like routes, except they use a different decorator: @Blueprint_name.app_errorandler()

#PARAM: The error itself
#RETURNS: Page template and a status code = 404
@errors.app_errorhandler(404)
def error_404(error):
    title = "Oh no! Page not found .. (404)"
    msg = "This page does not exist. Please check your route."
    return render_template('errors.html',title=title, msg=msg),404

#PARAM: The error itself
#RETURNS: page template and a status code = 403
@errors.app_errorhandler(403)
def error_403(error):
    title = "Sneaky! This is forbidden (403)"
    msg = "Check your credentials/account and try again"
    return render_template('errors.html',title=title, msg=msg),403

#PARAM: The error itself
#RETURNS: page template and a status code = 500
@errors.app_errorhandler(500)
def error_500(error):
    title = "Something messed up .. (500)"
    msg = "This is a general server error. So we are having trouble on our side. Sorry ):"
    return render_template('errors.html',title=title, msg=msg),500
