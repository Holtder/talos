from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .tasks import search_appstores_task
import enum
import os
import csv
import json
from .appstore import appresult
"""TM
I usually order my imports

standard library imports
#one enter
dependency imports
#one enter
internal imports
#two enters

This might be my OCD... Anyway, here it would be:

from datetime import datetime
import json
import enum
import csv
import os

from flask_sqlalchemy import SQLAlchemy

from .tasks import search_appstore_task
from .appstore import appresult
"""


db = SQLAlchemy()


class dbJob(db.Model):
    class State(enum.Enum):
        Waiting = 1
        Running = 2
        Finished = 3

    """ Database model representing a Job """
    id = db.Column(db.Integer, primary_key=True)

    jobname = db.Column(db.String(30), nullable=True,
                        default='No jobname supplied')
    countrycode = db.Column(db.String(2), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    terms = db.Column(db.String(), nullable=False)
    results = db.Column(db.Integer, nullable=True)
    state = db.Column(db.Enum(State), nullable=False)

    apps = db.relationship('dbApp', backref='by_job', lazy=True)

    @classmethod
    def start(cls, jobnumber):
        job = cls.query.get(jobnumber)

        if job is None or job.state != cls.State.Waiting:
            return False

        job.state = cls.State.Running
        search_appstores_task.delay(job.terms, job.countrycode, job.id)
        db.session.commit()
        return True

    @classmethod
    def cancel(cls, jobnumber):
        job = cls.query.get(jobnumber)

        if job is None or job.state != cls.State.Waiting:
            return False

        db.session.delete(job)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, jobnumber):
        job = cls.query.get(jobnumber)

        if job is None or job.state != cls.State.Finished:
            return False

        for app in job.apps:
            db.session.delete(app)

        # This should ideally be a constant somewhere
        outputPath = f'talos/static/output/{job.id}.csv'

        try:
            os.remove(outputPath)
        except OSError as ex:
            print(f"Error while deleting file {outputPath}, {ex}.")

        db.session.delete(job)
        db.session.commit()
        return True

    @classmethod
    def export(cls, jobnumber, filetype):
        """TM
        Readability could be improved here with:

        from sqlalchemy import inspect

        function dict(self):
            return {
                column.key: getattr(self, column.key)
                for column in inspect(self).mapper.column_attrs
            }

        function as_AppResult(self):
            return AppResult(AppResult.Source.Database, self.dict())

        @classmethod
        def export(...)
            ...
            results = [app.as_AppResult().dict() for app in job.apps]
        or

        @property
        function result(self):
            return AppResult(AppResult.Source.Database, self.dict())

        @classmethod
        def export(...)
            ...
            results = [app.result.dict() for app in job.apps]
        """
        job = cls.query.get(jobnumber)
        results = []

        for app in job.apps:
            result = appresult(appresult.Source.Database, **app.__dict__).dict()
            results.append(result)

        dirName = 'talos/static/output/'
        # Create target directory if doesn't exist yet
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        with open(f'{dirName}results.{filetype}', 'w') as exportFile:
            if filetype == 'CSV':
                """TM
                What does [*results[0]] do? I can of course look back and see it is the first
                result, then unpack it as a list, which gets me the keys. That is not very
                readable. Maybe add a appresult.keys()?
                """
                print([*results[0]])
                writer = csv.DictWriter(exportFile, delimiter=';', quoting=csv.QUOTE_MINIMAL, fieldnames=[*results[0]])
                writer.writeheader()
                for app in results:
                    writer.writerow(app)
            elif filetype == 'JSON':
                json.dump(results, exportFile)
        return True


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
