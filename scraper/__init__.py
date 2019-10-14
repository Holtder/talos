# Due to an unfortunate incident with Sharepoint all comments were lost, Currently in the process of rewriting them
import play_scraper
import requests
import time
import os
import csv
import json
import scraper.consts
from scraper.appstore import android_search, apple_search
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurations
# Setting up the main object all the Flask functions as based on.
webapp = Flask(__name__)
# Config that allows data validation, any random string will do, this is a 16
# character hex
webapp.config['SECRET_KEY'] = '857de896a3ad275824157a245a057f5c'
# URI (NOT URL) of the database, /// signifies a local path, this way we
# dont need to set up an account
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

# Allocation/instancing of the SQLAlchemy object
db = SQLAlchemy(webapp)

def search_appstores(arg_searchterm, arg_country):
    # Using consts may seem redundant, but this allows one output to be applied differently where necessary
    # This way there is room for the addition of other languages without adding too much work

    results = android_search(arg_searchterm, arg_country, 1)
    results += apple_search(arg_searchterm, arg_country)
    return results


# Function that exports a collection of appresult instances and allows for optional name specification
def export_csv(app_list, filename="output"):
    dirName = 'output'

    # Create target directory if doesn't exist yet
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

    # Actual exportation, overwrites the file if it exists
    with open('output/%s.csv' % (filename), 'w') as f:
        f.write("bundleid;store;app_title;description;dev_name;dev_id;fullprice;versionnumber;osreq;latest_patch;content_rating\n")
        for app in app_list:
            f.write("%s;" % (app.bundleid))
            f.write("%s;" % (app.store))
            f.write("%s;" % (app.app_title))
            f.write("%s;" % (app.description))
            f.write("%s;" % (app.dev_name))
            f.write("%s;" % (app.dev_id))
            f.write("%s;" % (app.fullprice))
            f.write("%s;" % (app.versionnumber))
            f.write("%s;" % (app.osreq))
            f.write("%s;" % (app.latest_patch.date()))
            f.write("%s" % (app.content_rating))
            f.write("\n")

from scraper import routes
