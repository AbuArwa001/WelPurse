from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class ContributionForm(FlaskForm):
    welfare_group = SelectField('Welfare Group', choices=[('', 'Select Welfare Group'), ('welfare1', 'Welfare 1'), ('welfare2', 'Welfare 2')], validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('mpesa', 'MPesa')], validators=[DataRequired()])
    # payment_method = SelectField('Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('mpesa', 'MPesa')], validators=[DataRequired()])
    mpesa_number = StringField('MPesa Number')
    welfare_id = HiddenField('Welfare ID')
    submit = SubmitField('Contribute Now')
