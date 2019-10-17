import os
from flask import render_template, url_for, flash, redirect, Blueprint
from .tasks import search_appstores_task
from .forms import AppQuery, JobAction
from .models import db, dbApp, dbJob

talosBP = Blueprint("Talos", __name__)

# Route for the home page, have information about the Scraper here
@talosBP.route('/')
@talosBP.route('/home')
def home():
    return render_template('home.html', title='Home')

# Route for the Submit Query page
@talosBP.route('/submitquery', methods=['GET', 'POST'])
def submitquery():
    # Pull AppQuery from forms.py so it can be used as an argument
    form = AppQuery()

    # Run this code if the form was valid and completed
    if form.validate_on_submit():
        job = dbJob(jobname=form.job_name.data, countrycode=form.shop_country.data, terms=form.query.data, state="Waiting")
        db.session.add(job)
        db.session.commit()

        # Set flash message to notify user of succesfull query submission.
        flash(f'Job {form.job_name.data} successfully submitted!', 'success')
        return redirect(url_for('Talos.jobs'))
    return render_template('submitquery.html', title='Submit a new Query',
                           form=form)

# This page shows all waiting, running and completed jobs and allows the user to download results
@talosBP.route('/jobs', methods=['GET', 'POST'])
def jobs():
    jobactionform = JobAction()

    if jobactionform.validate_on_submit():
        job = dbJob.query.get(jobactionform.jobnumber.data)
        if jobactionform.submitstart.data is True:
            job.state = "In Progress"
            db.session.commit()
            print("Calling task")
            task = search_appstores_task.delay(job.terms, job.countrycode, job.id)
            flash(f'Job {job.id} successfully started!', 'success')
        elif jobactionform.submitcancel.data is True:
            jobApps = dbApp.query.filter_by(job_id=job.id)
            for res in jobApps:
                db.session.delete(res)
            outputPath = f'talos/static/output/{job.id}.csv'
            try:
                os.remove(outputPath)
            except:
                print("Error while deleting file ", outputPath)
            db.session.delete(job)
            db.session.commit()
            flash(f'Job {job.id} successfully cancelled!', 'success')

    jobs = dbJob.query.all()
    return render_template('jobs.html', title='Current Jobs', jobs=jobs, jobactionform=jobactionform)


@talosBP.route('/about')
def about():
    return render_template('jobs.html', title="About us")
