#############################################################################################
#  PURPOSE: This contains key additional non-route methods relevant for the "tests" package #
#############################################################################################

from TestTracker.models import User, Test, ACT, PSAT, SAT #From TestTracker package, the models.py file defines these classes

#3rd party libraries -- Handles data maniputlation
import json #allows back and forth conversion between dictionaires and Strings
import pandas as pd #allows data storage as Pandas DataFrames, which operate like a multidimensional HashMap

#3rd party libraries -- Handles images/plot creation and rendering
import io #provides additional functionality for input/output
from matplotlib import pyplot as plt #Graphing utility
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas #Graphing utility
from matplotlib.figure import Figure #Graphing utility

#PARAM: User user, String type (of test)
#RETURNS: Pandas Dataframe of all that User's SATs OR ACTs OR PSATs. The DataFrame operates like a multi-dimensional HashMap
def get_testType_as_pandas_dataframe(user,type):
    #Gets all tests of a particular type by the user (ie all SATS by a User)
    user_tests = Test.query.filter_by(author=user,type=type)

    list_of_reports = []

    #For each test in user_tests, create a dictionary of that single Test's Date, score report (a new key per section) and cummulative score
    for test in user_tests:
        #INGENIOUS -- I create scores_dict to prevent repetition of json.loads in **scores_dict and calculate_cummulative_score(scores_dict)
        scores_dict = json.loads(test.report) #Converts the String test.report attribute into a Python dictionary (acts like a Java HashMap)
        new_row = {"Date":test.date_posted.strftime('%m/%d/%y'),
                    **scores_dict,
                    "Cummulative":test.calculate_cummulative_score(scores_dict)}
        list_of_reports.append(new_row) #appends this newly created dictionary describing the Test to the list_of_reports
    list_of_reports = pd.DataFrame(list_of_reports) #converts list_of_reports from List of dictionaries to a Pandas Dataframe .. keys = col headers
    return list_of_reports

#PARAM: String type (of test), Pandas dataframe (multidimensional HashMap) of all User's tests of that type
    #assumes df contains appropriate keys
#RETURNS: SCALABLE VECTOR GRAPHICS (SVG) expressed as a String
def plot_testType(type,df):
    #Creates/formats empty space for graphic to go
    fig = Figure()
    FigureCanvas(fig)
    plt.rcParams.update({'font.family':'fantasy'})

    #ERROR CHECK: If no tests added yet, displays a message to add tests
    if len(df) == 0:
        fig.text(0.7, 0.7, f"Please add a {type}!", size=55, ha="center", va="center",
                bbox=dict(boxstyle="round",ec=(1., 0.05, 0.05),fc=(0.59,0.45,0.67,0.3)))
    #Else, creates the graph
    else:
        ax = fig.add_subplot(111)
        plot_df = df.copy() #INGENIOUS -- Creates a shallow copy, so original datatable is NOT modified!!
        plot_df.reset_index(drop=False,inplace=True)

        ax.set_title(f'{type.upper()} Progress Graph')
        ax.grid(True)

        ax.set_xlabel('Test Number')
        ax.set_xticks(list(range(0,len(df)+2,1))) #Creates the min, max of x-values: Will range from [0, length+2) with discreate interval = 1
        ymax = -1
        yint = -1

        num_series = 0 #num_series = number of series plotted .. needed to build/format the legend
        ax.plot(plot_df["index"].apply(str), plot_df["Cummulative"],marker="o",label="Cummulative",color="k") #plots Cummulative scores
        num_series+=1 #Because we just added the Cummulative Series

        #Plots section scores based on test type
        if type == 'PSAT':
            ymax=1520
            yint = 100
            ax.plot(plot_df["index"].apply(str), plot_df["EBRW"],marker="o",label="EBRW",linestyle='dashed')
            ax.plot(plot_df["index"].apply(str), plot_df["Math"],marker="o",label="Math",linestyle='dashed')
            num_series+=2
        elif type == 'SAT':
            ymax=1600
            yint = 100
            ax.plot(plot_df["index"].apply(str), plot_df["EBRW"],marker="o",label="EBRW",linestyle='dashed')
            ax.plot(plot_df["index"].apply(str), plot_df["Math"],marker="o",label="Math",linestyle='dashed')
            num_series+=2
        else:
            ymax=36
            yint=6
            ax.plot(plot_df["index"].apply(str), plot_df["English"],marker="o",label="English",linestyle='-.')
            ax.plot(plot_df["index"].apply(str), plot_df["Math"],marker="o",label="Math",linestyle='-.')
            ax.plot(plot_df["index"].apply(str), plot_df["Reading"],marker="o",label="EBRW",linestyle='-.')
            ax.plot(plot_df["index"].apply(str), plot_df["Science"],marker="o",label="Math",linestyle='-.')
            num_series+=4

        ax.set_yticks(list(range(0,ymax+yint,yint))) #Creates the min, max of y-values: Will range from [0,ymax+100) with discreate intervals = 100
        ax.set_ylabel('Score')
        fig.legend(bbox_to_anchor=(0, -0.06, 1, 1), loc="lower left", mode="expand",ncol=num_series)


    #Saves/returns figure as an SVG = SCALABLE VECTOR GRAPHICS (SVG)
    img = io.StringIO()
    fig.savefig(img, format='svg',bbox_inches='tight')
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    return svg_img
