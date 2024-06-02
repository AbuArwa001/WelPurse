from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional

class ContributionForm(FlaskForm):
    welfare_group = HiddenField('Welfare Group', validators=[Optional()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    # payment_method = HiddenField('Payment Method', validators=[DataRequired()])
    # payment_method = SelectField('Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('mpesa', 'MPesa')], validators=[DataRequired()])
    mpesa_number = StringField('MPesa Number')
    welfare_id = HiddenField('Welfare ID')
    event_id = HiddenField('Welfare ID')
    submit = SubmitField('Contribute Now')
