from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class dbJob(db.Model):
    """ Database model representing a Job """
    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(30), nullable=True,
                        default='No jobname supplied')
    countrycode = db.Column(db.String(2), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    terms = db.Column(db.String(), nullable=False)
    results = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(), nullable=False)
    apps = db.relationship('dbApp', backref='by_job', lazy=True)


class dbApp(db.Model):
    """ Database model representing one result of Job query """
    id = db.Column(db.Integer, primary_key=True)
    app_title = db.Column(db.String(), nullable=False)
    store = db.Column(db.String(), nullable=False)
    bundleid = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    dev_name = db.Column(db.String(), nullable=False)
    dev_id = db.Column(db.String(), nullable=False)
    fullprice = db.Column(db.Integer, nullable=False)
    versionnumber = db.Column(db.String(), nullable=False)
    osreq = db.Column(db.String(), nullable=False)
    latest_patch = db.Column(db.String(), nullable=False)
    content_rating = db.Column(db.String(), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('db_job.id'), nullable=False)
