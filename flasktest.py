from flask import Flask, render_template, url_for, flash, redirect
from forms import AppQuery

# Setting up the main object all the Flask functions as based on.
app = Flask(__name__)
app.config['SECRET_KEY'] = '857de896a3ad275824157a245a057f5c'

# Route for the home page, have information about the Scraper here
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# Route for the Submit Query page
@app.route('/submitquery', methods=['GET','POST'])
def submitquery():
    # Pull AppQuery from forms.py so it can be used as an argument
    form = AppQuery()

    # Run this code if the form was completed and the user was redirected to this page
    if form.validate_on_submit():
        # Set flash message to notify user of succesfull query submission.
        flash(f'Job {form.job_name.data} successfully submitted!', 'success')
        return redirect(url_for('submitquery'))
    return render_template('submitquery.html', title='Submit a new Query', form=form)


@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Current Jobs')

if __name__ == '__main__':
    # Turn debug off when used on server!
    app.run(debug=True)