##################################################################################
#  PURPOSE: This file contains all the routes relevant to the "tests" Blueprint  #
##################################################################################

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, make_response #3rd party
from flask_login import current_user, login_required #3rd party
import json #3rd party
from TestTracker import db #From TestTracker package, the __init__.py file defines this variable
from TestTracker.models import User, Test, ACT, PSAT, SAT #From TestTracker package, the models.py file defines these classes
from TestTracker.tests.forms import PSATForm, SATForm, ACTForm #From tests subpackage, the forms.py defines these classes
from TestTracker.tests.utils import get_testType_as_pandas_dataframe, plot_testType #From tests subpackage, the utils.py defines these methods

tests = Blueprint("tests", __name__) #instantiates a Blueprint object called "tests" .. this adds modularity to this tests package

#This @Blueprint_name.route decorator adds Link/route functionality to the method

############################################################################
###                              TESTS                                  ###
############################################################################

#PARAM: String type ... this is the type of tests: PSAT, SAT, ACT
#RETURNS: The appropriate template, based on type chosen
@tests.route('/<string:type>/new', methods=['GET','POST'])
@login_required
def new_test(type):
    if type == 'PSAT':
        form = PSATForm() #instantiates PSATForm object
        #Checks if form passes all the validation checks. If so, commits changes to database
        if form.validate_on_submit():
            score_report = {"EBRW":form.ebrw.data, "Math":form.math.data} #Buillds dictionary that will be conversted to String via JSON
            psat = PSAT(report=json.dumps(score_report), author=current_user) #Instantiates a PSAT object
            db.session.add(psat) #Saves PSAT to database
            db.session.commit()
            flash("Your PSAT has been added!",'success')
            return redirect(url_for('users.home',username=current_user.username)) #Redirects to the Home route, for you to see your tests
        #If the form does not validate or has not been submitted, continues to show create_psat template in the new_test route
        return render_template('create_psat.html',title='New PSAT Test', form=form, legend='New PSAT Test')

    elif type == 'SAT':
        form = SATForm() #instantiates SATForm object
        #Checks if form passes all the validation checks. If so, commits changes to database
        if form.validate_on_submit():
            score_report = {"EBRW":form.ebrw.data, "Math":form.math.data} #Buillds dictionary that will be conversted to String via JSON
            sat = SAT(report=json.dumps(score_report), author=current_user) #Instantiates a SAT object
            db.session.add(sat) #Saves SAT into database
            db.session.commit()
            flash("Your SAT has been added!",'success')
            return redirect(url_for('users.home',username=current_user.username)) #Redirects to the Home route, for you to see your tests
        #If the form does not validate or has not been submitted, continues to show create_sat template in the new_test route
        return render_template('create_sat.html',title='New SAT Test', form=form, legend='New SAT Test')

    else:
        form = ACTForm() #instantiates ACTFrom object
        #Checks if form passes all the validation checks. If so, commits changes to database
        if form.validate_on_submit():
            score_report = {"English":form.english.data, "Math":form.math.data,
                            "Reading":form.reading.data, "Science":form.science.data} #Buillds dictionary that will be conversted to String via JSON
            act = ACT(report=json.dumps(score_report), author=current_user) #Instantiates an ACT object
            db.session.add(act) #Saves ACT into database
            db.session.commit()
            flash("Your ACT has been added!",'success')
            return redirect(url_for('users.home',username=current_user.username)) #Redirects to the Home route, for you to see your tests
        #If the form does not validate or has not been submitted, continues to show create_act template in the new_test route
        return render_template('create_act.html',title='New ACT Test', form=form, legend='New ACT Test')

#PARAM: int test_id
#RETURNS: test.html template
@tests.route('/test/<int:test_id>')
@login_required
def test(test_id):
    #Either retrive and display the test or return a 404 error if test does not exist
    test = Test.query.get_or_404(test_id)
    #Prevents User from seeing other User's tests
    if test.author != current_user:
        abort(403)
    test_title = f"{test.type} - {test.date_posted.strftime('%b %d, %Y')}"
    return render_template('test.html',title=test_title, test=test)

#PARAM: String type ... this is the type of tests: PSAT, SAT, ACT
#RETURNS: The appropriate template, based on type chosen
@tests.route('/test/<int:test_id>/update', methods=['GET','POST'])
@login_required
def update_test(test_id):
    #Either retrive and display the test or return a 404 error if test Does not exist in the database
    test = Test.query.get_or_404(test_id)
    #Prevents User from updating other User's tests
    if test.author != current_user:
        abort(403)
    report_dict = json.loads(test.report) #Uses JSON to convert String test.report into a Python dictionary
    #Creates form appropriate for test type
    if str(test.type) == 'PSAT':
        form = PSATForm() #Instantiates PSATForm
        #Checks if form passes all the validation checks. If so, commits changes to database
        if form.validate_on_submit():
            report_dict["EBRW"] = form.ebrw.data #Modies ebrw section score in the report_dict Dictionary with form input
            report_dict["Math"] = form.math.data #Modies math section score in the report_dict Dictionary with form input
            test.report = json.dumps(report_dict) #Converts this report_dict to String via JSON
            db.session.commit() #Saves changes in database
            flash("Your PSAT has been updated!",'success')
            return redirect(url_for('tests.test',test_id=test.id))
        #Unless you are filling out the field, the fields are pre-populated with the current section scores
        elif request.method == 'GET':
            form.ebrw.data = report_dict["EBRW"] #Prepopulates EBRW
            form.math.data = report_dict["Math"] #Prepopulates Math
        #If the form does not validate or has not been submitted, continues to show create_psat template in the nupdate_test route
        return render_template('create_psat.html',title='Update PSAT Test', form=form, legend='Update PSAT Test')
    elif str(test.type) == 'SAT':
        form = SATForm() #Instantiates SATForm
        #Checks if form passes all the validation checks. If so, commits changes to database
        if form.validate_on_submit():
            report_dict["EBRW"] = form.ebrw.data #Modies ebrw section score in the report_dict Dictionary with form input
            report_dict["Math"] = form.math.data #Modies math section score in the report_dict Dictionary with form input
            test.report = json.dumps(report_dict) #Converts this report_dict to String via JSON
            db.session.commit() #Saves changes in database
            flash("Your SAT has been updated!",'success')
            return redirect(url_for('tests.test',test_id=test.id))
        #Unless you are filling out the field, the fields are pre-populated with the current section scores
        elif request.method == 'GET':
            form.ebrw.data = report_dict["EBRW"] #Prepopulates EBRW
            form.math.data = report_dict["Math"] #Prepopulates Math
        #If the form does not validate or has not been submitted, continues to show create_psat template in the update_test route
        return render_template('create_sat.html',title='Update SAT Test', form=form, legend='Update SAT Test')
    else:
        form = ACTForm() #Instantiates ACTForm
        #Checks if form passes all the validation checks. If so, commits changes to database
        if form.validate_on_submit():
            report_dict["English"] = form.english.data #Modies English section score in the report_dict Dictionary with form input
            report_dict["Math"] = form.math.data #Modies Math section score in the report_dict Dictionary with form input
            report_dict["Reading"] = form.reading.data #Modies Reading section score in the report_dict Dictionary with form input
            report_dict["Science"] = form.science.data #Modies Science section score in the report_dict Dictionary with form input
            test.report = json.dumps(report_dict) #Converts this report_dict to String via JSON
            db.session.commit() #Saves changes in database
            flash("Your ACT has been updated!",'success')
            return redirect(url_for('tests.test',test_id=test.id))
        #Unless you are filling out the field, the fields are pre-populated with the current section scores
        elif request.method == 'GET':
            form.english.data = report_dict["English"] #Prepopulates English
            form.math.data = report_dict["Math"] #Prepopulates Math
            form.reading.data = report_dict["Reading"] #Prepopulates Reading
            form.science.data = report_dict["Science"] #Prepopulates Science
        #If the form does not validate or has not been submitted, continues to show create_psat template in the update_test route
        return render_template('create_act.html',title='Update ACT Test', form=form, legend='Update ACT Test')

#PARAM: int test_id
#RETURNS: Response to go to home.html template
@tests.route('/test/<int:test_id>/delete', methods=['POST'])
@login_required
def delete_test(test_id):
    #Either retrive and display the test or return a 404 error if test Does not exist in database
    test = Test.query.get_or_404(test_id)
    #Prevents users from updating other user tests
    if test.author != current_user:
        abort(403)
    db.session.delete(test) #Deletes Test
    db.session.commit() #Saves changes
    flash(f"Your {test.type} has been deleted!",'success')
    #Redirects User to their Home Page
    return redirect(url_for('users.home',username=current_user.username))

############################################################################
###                         OTHER FUNCTIONALITY                          ###
############################################################################

#PARAM: int user_id, String type
#RETURNS:
@tests.route('/view_test/<int:user_id>/<string:type>',methods=['GET'])
@login_required
def view_test_progress(user_id,type):
    #Checks current_user matches the user whose data I try to access
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    df = get_testType_as_pandas_dataframe(user,type) #from utils.py
    #ERROR CHECK: If there are NO TEST YET! Do NOT show a table
    if len(df) == 0:
        html_df = ""
    #Else: create the HTML code to build the table
    else:
        df.reset_index(drop=True, inplace=False)
        df.index += 1 #Ensures the user sees the Test count begins from 1 (> user friendly than starting from 0)
        df.rename(columns={"index":"Test #"})
        html_df = df.to_html(classes=["test"],bold_rows=False)
    plot = plot_testType(type,df) #from utils.py
    #Returns created template view_test.html with the plot, table, and type passed in as parameters
    return render_template("view_test.html",plot=plot,table=html_df,type=type)

@tests.route('/view_test/<int:user_id>/<string:type>/download')
@login_required
def download_report(user_id,type):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    scores_df = get_testType_as_pandas_dataframe(user,type)
    filename = user.username + "_" + type + "_report" +'.csv'
    scores_df.reset_index(drop=True, inplace=True)
    if len(scores_df) == 0:
        flash(f"You do not have any records to download. Please add a {type}","danger")
        return redirect(url_for("tests.view_test_progress",user_id=user_id, type=type))
    resp = make_response(scores_df.to_csv())
    resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
    resp.headers["Content-Type"] = "text/csv"
    flash("Your file has successfully downloaded!","success")
    return resp
