##################################################################################
#  PURPOSE: This file contains all the routes relevant to the "users" Blueprint  #
##################################################################################

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort  #3rd party
from flask_login import login_user, current_user, logout_user, login_required   #3rd party
from TestTracker import db, bcrypt  #From TestTracker package, the __init__.py file defines these variables
from TestTracker.models import User, Test, SAT, PSAT, ACT #From TestTracker package, the models.py file defines these classes
from TestTracker.users.forms import RegistrationForm, LoginForm, UpdateAccountForm #From users subpackage, the forms.py defines these classes

users = Blueprint("users", __name__)    #instantiates a Blueprint object called "users" .. this adds modularity to this users package

#This @Blueprint_name.route decorator adds Link/route functionality to the method

#PARAM: String username
#RETURNS: A response to render the home.html template, a page with all User's tests
@users.route('/home/<string:username>')
@login_required
def home(username):
    #Searches SQLite database for User with given username. Checks if matches current_user, throwing a 403 error if false.
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if username != current_user.username:
        abort(403)

    #page is a request. ... in the URL, this appears as /home/username?page=1
    page = request.args.get('page',1,type=int)  #By setting type as int, it will throw a value error URL contains a type = anything other than int

    #Searches SQLite database for all Tests authored by current_user. Passes paginated display in descending order as a List into template
    tests = Test.query.filter_by(author=user).order_by(Test.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', tests=tests, user=user)

############################################################################
###                                USER                                  ###
############################################################################

#PARAM: None
#RETURNS: A response to an html template
@users.route('/register', methods=['GET','POST']) #GET allows access of this route's data. POST allows you to submit onto the same route
def register():
    #ERROR CHECK: If you are already logged in, then you cannot access the RegistrationForm. It redirects you to the Home page
    if current_user.is_authenticated:
        return redirect(url_for('users.home',username=current_user.username))

    #If you are not yet logged in, then you CAN access the RegistrationForm
    form = RegistrationForm() #instantiates RegistrationForm that is sent to register.html template

    #Checks if form passes all the validation checks. If so, commits changes to database
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #Hashes password using Bcrypt module
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #instantiates User with form data
        db.session.add(user) #saves User into database
        db.session.commit()
        flash(f"Account successfully created! :D", 'success')
        return redirect(url_for('users.login')) #Redirects to the Login route, for you to login with newly created credentials

    #If the form does not validate or has not been submitted, continues to show register route
    return render_template('register.html',title='Register', form=form)

#PARAM: None
#RETURNS: A response to an html template
@users.route('/login', methods=['GET','POST']) #GET allows access of this route's data. POST allows you to submit onto the same route
def login():
    #ERROR CHECK: If you are already logged in, then you cannot access the LoginForm. It redirects you to the Home page
    if current_user.is_authenticated:
        return redirect(url_for('users.home',username=current_user.username))

    #If you are not yet logged in, then you CAN access the LoginForm
    form = LoginForm() #instantiates LoginForm that is sent to login.html template

    #Checks if form passes all the validation checks. If so, checks form input with database
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #If there is a User with the same email and the same unhashed password as the form inputs, then logins User
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            #If you were trying to access a forbidden page, it then navigates you to that page that you were tryna access. Else, navigates to home
            next_page = request.args.get('next')
            flash(f"Hello {user.username}!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('users.home',username=current_user.username))
        else:
            flash("Login Unsuccessful. Please check your credentials", 'danger')

    #If the form does not validate or has not been submitted or credentials do not match anything in database, continues to show login route
    return render_template('login.html',title='Login', form=form)

#PARAM: None
#RETURNS: A redirect to the about.html template
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.about'))


############################################################################
###                              ACCOUNT                                 ###
############################################################################

#PARAM: None
#RETURNS: A response to the account.html template
@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()  #instantiates an UpdateAccountForm

    #Checks if form passes all the validation checks, once the form is submitted. If so, committs changes to database
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has updated successfully!", 'success')
        return redirect(url_for('users.account'))
    #If we still accept data (Not yet hit submit), pre-populates the fields with the current username and email
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    #If the form does not validate or has not been submitted, then continues to show the account route
    return render_template('account.html',title='Account', form=form)

#PARAM: int user_id
#RETURNS: A redirect to the initial 'about' page, after the User and their Tests are deleted from the SQLite database
@users.route('/account/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_account(user_id):
    #Checks if account matches current user. If not, then throws a 403 forbidden Access error
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)

    #First, delete all tests by that user from Test table
    user_tests = Test.query.filter_by(author=user)
    for test in user_tests:
        db.session.delete(test)

    #Then, delete user from User table
    db.session.delete(user)

    #Commits all changes to both datatables
    db.session.commit()
    flash("Your account has been deleted successfully!","success")

    #Returns to the start page, about.html
    return redirect(url_for('main.about'))
