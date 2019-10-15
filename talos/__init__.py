# Due to an unfortunate incident with Sharepoint all comments were lost, Currently in the process of rewriting them
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from datetime import datetime
from talos.appstore import search_appstores, export_csv

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
webapp.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
webapp.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(webapp.name, broker=webapp.config['CELERY_BROKER_URL'])
celery.conf.update(webapp.config)

# Allocation/instancing of the SQLAlchemy object
db = SQLAlchemy(webapp)
from talos.models import dbApp, dbJob
db.create_all()

@celery.task
def search_appstores_task(term, country, jobid):
    print(f"Starting Task for job ({jobid})")
    job = dbJob.query.get(jobid)
    results = search_appstores(term, country)
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
    job.results = len(results)
    job.state = "Complete"
    db.session.add(job)
    db.session.commit()
    export_csv(results, jobid)
    print(f"Completed Task for Job({job.id}), found {job.results} apps.")
    return 1

from talos import routes
