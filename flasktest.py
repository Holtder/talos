from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import AppQuery

# Configurations
# Setting up the main object all the Flask functions as based on.
app = Flask(__name__)
# Config that allows data validation, any random string will do, this is a 16
# character hex
app.config['SECRET_KEY'] = '857de896a3ad275824157a245a057f5c'
# URI (NOT URL) of the database, /// signifies a local path, this way we
# dont need to set up an account
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Allocation/instancing of the SQLAlchemy object
db = SQLAlchemy(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(30), nullable=True,
                        default='No jobname supplied')
    country_code = db.Column(db.String(2), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    terms = db.Column(db.String(), nullable=False)
    results = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        # A magic python function that is called when printing the class instance
        return f"Job: ({self.country_code}) {self.jobname} \n {self.terms}"

# Route for the home page, have information about the Scraper here
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# Route for the Submit Query page
@app.route('/submitquery', methods=['GET', 'POST'])
def submitquery():
    # Pull AppQuery from forms.py so it can be used as an argument
    form = AppQuery()

    # Run this code if the form was valid and completed
    if form.validate_on_submit():
        # Set flash message to notify user of succesfull query submission.
        flash(f'Job {form.job_name.data} successfully submitted!', 'success')
        return redirect(url_for('submitquery'))
    return render_template('submitquery.html', title='Submit a new Query',
                           form=form)


@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Current Jobs')


@app.route('/about')
def about():
    return render_template('jobs.html', title="About us")


if __name__ == '__main__':
    # Turn debug off when used on server!
    app.run(debug=True)
