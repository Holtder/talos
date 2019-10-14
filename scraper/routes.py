from flask import render_template, url_for, flash, redirect
from scraper import webapp, db
from scraper.forms import AppQuery
from scraper.models import dbApp, dbJob

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


@webapp.route('/jobs')
def jobs():
    jobs = dbJob.query.all()
    print(jobs[0].jobname)
    return render_template('jobs.html', title='Current Jobs', jobs=jobs)


@webapp.route('/about')
def about():
    return render_template('jobs.html', title="About us")
