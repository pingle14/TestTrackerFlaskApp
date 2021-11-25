#########################################################################################
#  PURPOSE: This file is is a MODULE that runs the app, acting as the main/runner       #
#########################################################################################

from TestTracker import app #Imports app from TestTracker package ... aka imports from TestTracker's __init__.py file where app is instantiated

#Checks if this file is the main, which it is by definition, before running the app
if __name__ == '__main__':
    app.run(debug=True)
