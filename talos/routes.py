import threading
from flask import render_template, url_for, flash, redirect
from talos import webapp, db
from talos.forms import AppQuery, JobAction
from talos.models import dbApp, dbJob

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
        job = dbJob(jobname=form.job_name.data, countrycode=form.shop_country.data, terms=form.query.data)
        db.session.add(job)
        db.session.commit()

        # Set flash message to notify user of succesfull query submission.
        flash(f'Job {form.job_name.data} successfully submitted!', 'success')
        return redirect(url_for('jobs'))
    return render_template('submitquery.html', title='Submit a new Query',
                           form=form)


@webapp.route('/jobs', methods=['GET', 'POST'])
def jobs():
    jobactionform = JobAction()

    if jobactionform.validate_on_submit():
        job = dbJob.query.get(jobactionform.jobnumber.data)
        if jobactionform.submitstart.data is True:
            job.state = "In Progress"
            flash(f'Job {job.id} successfully started!', 'success')
        elif jobactionform.submitcancel.data is True:
            db.session.delete(job)
            db.session.commit()
            flash(f'Job {job.id} successfully cancelled!', 'success')

    jobs = dbJob.query.all()
    return render_template('jobs.html', title='Current Jobs', jobs=jobs, jobactionform=jobactionform)


@webapp.route('/about')
def about():
    return render_template('jobs.html', title="About us")
