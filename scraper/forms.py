from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

COUNTRY_ABBREV = [('us', 'United States'), ('gb', 'Great Britain'), ('nl', 'The Netherlands')]

class AppQuery(FlaskForm):
    query = StringField('Search Terms:', validators=[DataRequired(), Length(min=3)])
    shop_country = SelectField('Simulated country of request:', choices=COUNTRY_ABBREV)
    job_name = StringField('Job Name:', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Submit')
