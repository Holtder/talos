from flask import render_template, url_for, flash, redirect, Blueprint
from .forms import AppQuery, JobAction
from .models import db, dbJob

talosBP = Blueprint("Talos", __name__, static_folder='static', static_url_path='/static')


@talosBP.route('/')
@talosBP.route('/home')
def home():
    """ Route for the home page, have information about the Scraper here """

    return render_template('home.html', title='Home')


@talosBP.route('/submitquery', methods=['GET', 'POST'])
def submitquery():
    """ # Route for the Submit Query page """

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


@talosBP.route('/jobs', methods=['GET', 'POST'])
def jobs():
    """ This page shows all waiting, running and completed jobs and allows the user to download results """
    jobactionform = JobAction()

    if jobactionform.validate_on_submit():
        job = dbJob.query.get(jobactionform.jobnumber.data)
        if jobactionform.submitstart.data is True:
            dbJob.start(job.id)
            flash(f'Job {job.id} successfully started! This WILL take a few minutes, grab some coffee!', 'success')
        elif jobactionform.submitcancel.data is True:
            dbJob.cancel(job.id)
            flash(f'Job {job.id} successfully canceled!', 'success')
        elif jobactionform.submitdelete.data is True:
            dbJob.delete(job.id)
            flash(f'Job {job.id} successfully deleted!', 'success')

    jobs = dbJob.query.all()
    return render_template('jobs.html', title='Current Jobs', jobs=jobs, jobactionform=jobactionform)


@talosBP.route('/results<jobid>.<type>')
def results(type, jobid):
    dbJob.export(jobid, type)
    return talosBP.send_static_file(f'output/results.{type}')


@talosBP.route('/about')
def about():
    return render_template('jobs.html', title="About us")
