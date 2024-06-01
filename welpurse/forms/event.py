from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    welfare_group_name = StringField('Welfare Group Name', validators=[DataRequired()], render_kw={'readonly': True})
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'readonly': True})
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'readonly': True})
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'readonly': True})
    donation_purpose = TextAreaField('Event Description', validators=[DataRequired()], render_kw={'readonly': True})
    amount_requested = IntegerField('Amount Needed', validators=[DataRequired()], render_kw={'readonly': True})
    submit = SubmitField('Create Event')





