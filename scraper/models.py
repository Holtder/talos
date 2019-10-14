from datetime import datetime
from scraper import db

class dbJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(30), nullable=True,
                        default='No jobname supplied')
    country_code = db.Column(db.String(2), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    terms = db.Column(db.String(), nullable=False)
    results = db.Column(db.Integer, nullable=True)
    apps = db.relationship('dbApp', backref='by_job', lazy=True)

    def __repr__(self):
        # A magic python function that is called when printing the class instance
        return f"Job: ({self.country_code}) {self.jobname} \n {self.terms}"

class dbApp(db.Model):
    job_id = db.Column(db.Integer, db.ForeignKey('db_job.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
