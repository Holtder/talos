import os
from flask import render_template, url_for, flash, redirect
from talos import webapp, db, celery, search_appstores_task
from talos.forms import AppQuery, JobAction
from talos.models import dbApp, dbJob
from celery.result import AsyncResult

# Route for the home page, have information about the Scraper here
@webapp.route('/')
@webapp.route('/home')
def home():
    return render_template('home.html', title='Home')

# Route for the Submit Query page
@webapp.route('/submitquery', methods=['GET', 'POST'])
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
        return redirect(url_for('jobs'))
    return render_template('submitquery.html', title='Submit a new Query',
                           form=form)

# This page shows all waiting, running and completed jobs and allows the user to download results
@webapp.route('/jobs', methods=['GET', 'POST'])
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
            except Exception as ex:
                print("Error while deleting file ", outputPath)
            db.session.delete(job)
            db.session.commit()
            flash(f'Job {job.id} successfully cancelled!', 'success')

    jobs = dbJob.query.all()
    return render_template('jobs.html', title='Current Jobs', jobs=jobs, jobactionform=jobactionform)


@webapp.route('/about')
def about():
    return render_template('jobs.html', title="About us")
