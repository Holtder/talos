from datetime import datetime
from talos import db

class dbJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(30), nullable=True,
                        default='No jobname supplied')
    countrycode = db.Column(db.String(2), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    terms = db.Column(db.String(), nullable=False)
    results = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(), nullable=False, default="Waiting")
    apps = db.relationship('dbApp', backref='by_job', lazy=True)

    def __repr__(self):
        # A magic python function that is called when printing the class instance
        return f"Job: ({self.country_code}) {self.jobname} \n {self.terms}"

class dbApp(db.Model):
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
    latest_patch = db.Column(db.DateTime, nullable=False)
    content_rating = db.Column(db.String(), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('db_job.id'), nullable=False)
