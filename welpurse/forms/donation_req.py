from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class DonationRequestForm(FlaskForm):
    reason = StringField('Reason for Donation', validators=[DataRequired()])
    amount_requested = DecimalField('Amount Requested', validators=[DataRequired()])
    submit = SubmitField('Confirm Donation')
