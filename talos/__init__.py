from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from datetime import datetime
from talos.appstore import search_appstores, export_csv

# Configurations
# Setting up the main object and all configsall the Flask functions as based on.
webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = '857de896a3ad275824157a245a057f5c'
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
webapp.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
webapp.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Tool that allows background tasks to run; in order to work, first run:
# $ redis-server --daemonize yes && celery -A talos.celery worker
celery = Celery(webapp.name, broker=webapp.config['CELERY_BROKER_URL'])
celery.conf.update(webapp.config)

# Allocation/instancing of the SQLAlchemy object
db = SQLAlchemy(webapp)
from talos.models import dbApp, dbJob
db.create_all()

# The one task in celery, unfortunately cannot be put into another module
@celery.task
def search_appstores_task(term, country, jobid):
    # Gets the job object from the ID that is passed
    job = dbJob.query.get(jobid)
    results = search_appstores(term, country)

    # Each app in results is stored in the DB
    for result in results:
        newApp = dbApp(app_title=str(result.app_title),
                       store=result.store,
                       bundleid=result.bundleid,
                       description=result.description,
                       dev_name=result.dev_name,
                       dev_id=result.dev_id,
                       fullprice=result.fullprice,
                       versionnumber=result.versionnumber,
                       osreq=result.osreq,
                       latest_patch=str(result.latest_patch.date()),
                       content_rating=result.content_rating[0],
                       job_id=jobid)
        db.session.add(newApp)
        db.session.commit()

    # For clarity on the webpage the total amount of results is stored
    job.results = len(results)
    job.state = "Complete"
    db.session.add(job)
    db.session.commit()
    export_csv(results, jobid)
    return 1  # No need to actually return anything

from talos import routes
