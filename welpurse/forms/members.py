from flask_wtf import FlaskForm
import requests
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('Full Names',
                           validators=[DataRequired(),
                            Length(min=3, max=20),
                                              ])
    email = StringField('Email',
                       validators=[DataRequired(),
                        Email()])
    password =  PasswordField('Password',
                              validators=[DataRequired()])
    confirm_password =  PasswordField('Password',
                              validators=[DataRequired(),
                            EqualTo('password')])
    submit = SubmitField('SIGN UP')

    def validate_email(self, email):
        api_endpoint = 'http://127.0.0.1:5001/api/v1/check_email'
        response = requests.get(api_endpoint, params={'email': email.data})
        if response.status_code == 200:
            email_exists = response.json().get('email_exists')
            if email_exists:
                raise ValidationError('That email is taken. Please choose a different one.')
        else:
            # Handle the case where the API is not reachable or returns an error
            raise ValidationError('Unable to validate email at this time. Please try again later.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired(),
                        Email()])
    password =  PasswordField('Password',
                              validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
