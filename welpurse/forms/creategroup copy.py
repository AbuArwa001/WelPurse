from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, RadioField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Optional

class WelfareGroupForm(FlaskForm):
    # Group Details
    welfare_name = StringField('Welfare Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    purpose = TextAreaField('Purpose for Group', validators=[Optional()])

    # Membership Criteria
    min_contribution = SelectField('Minimum Contribution', choices=[
        ('15000', '15,000'),
        ('20000', '20,000'),
        ('26000', '26,000'),
        ('35000', '35,000'),
        ('37000', '37,000'),
        ('above', 'Above 37,000')
    ], validators=[DataRequired()])
    
    eligibility_requirements = SelectMultipleField('Eligibility Requirement', choices=[
        ('15000-20000', '15,000 - 20,000'),
        ('26000-35000', '26,000 - 35,000'),
        ('37000-above', '37,000 - Above')
    ], validators=[Optional()])

    membership_approval = RadioField('Membership Approval', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ], validators=[DataRequired()])

    # Contribution Settings
    contribution_frequency = SelectField('Contribution Frequency', choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Per Annum')
    ], validators=[DataRequired()])
    
    contribution_modes = SelectMultipleField('Contribution Mode', choices=[
        ('mpesa', 'Mpesa'),
        ('card', 'Card'),
        ('paypal', 'PayPal')
    ], validators=[Optional()])
    
    special_events = BooleanField('Special Events')

    # Role Assignments
    administrator = SelectField('Administrator', choices=[('member', 'Select Member')], validators=[DataRequired()])
    treasurer = SelectField('Treasurer', choices=[('member', 'Select Member')], validators=[DataRequired()])
    secretary = SelectField('Secretary', choices=[('member', 'Select Member')], validators=[DataRequired()])
    youth_rep = SelectField('Youth Rep', choices=[('member', 'Select Member')], validators=[DataRequired()])
    chairperson = SelectField('Chairperson', choices=[('member', 'Select Member')], validators=[DataRequired()])
    vice_chairperson = SelectField('Vice Chairperson', choices=[('member', 'Select Member')], validators=[DataRequired()])

    # Role Descriptions
    role_description_chairperson = StringField('Chairperson', validators=[Optional()])
    role_description_vice_chair = StringField('Vice Chair', validators=[Optional()])
    role_description_treasurer = StringField('Treasurer', validators=[Optional()])
    role_description_secretary = StringField('Secretary', validators=[Optional()])
    role_description_youth_rep = StringField('Youth Rep', validators=[Optional()])

    # Visibility
    visibility = SelectField('Group Visibility', choices=[
        ('public', 'Public'),
        ('private', 'Private'),
        ('restricted', 'Restricted')
    ], validators=[DataRequired()])
    
    searchable = RadioField('Searchable', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ], validators=[DataRequired()])

    # Communication
    preferred_communication_channel = SelectField('Preferred Communication Channel', choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('app', 'In-App Messaging')
    ], validators=[DataRequired()])
    
    notification_preferences = SelectMultipleField('Notification Preference', choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('app', 'In-App')
    ], validators=[Optional()])

    submit = SubmitField('Submit')
