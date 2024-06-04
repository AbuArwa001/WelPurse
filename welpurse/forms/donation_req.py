from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class DonationRequestForm(FlaskForm):
    reason = StringField('Reason for Donation', validators=[DataRequired()])
    amount_requested = DecimalField('Amount Requested', validators=[DataRequired()])
    welfare_id = HiddenField('Welfare ID')
    member_id = HiddenField('MEMBER ID')
    request_id = HiddenField('Request ID')
    submit = SubmitField('Confirm Donation')
