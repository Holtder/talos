from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from .consts import COUNTRY_ABBREV


class AppQuery(FlaskForm):
    query = StringField('Search Terms:', validators=[DataRequired(), Length(min=3)])
    shop_country = SelectField('Simulated country of request:', choices=COUNTRY_ABBREV)
    job_name = StringField('Job Name:', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Submit')


class JobAction(FlaskForm):
    jobnumber = IntegerField('Job Number:', validators=[DataRequired()])
    submitstart = SubmitField('Start')
    submitcancel = SubmitField('Cancel')
    submitdelete = SubmitField('Delete')
