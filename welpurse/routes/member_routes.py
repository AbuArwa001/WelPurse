#welpurse/routes/member_routes.py
from flask import render_template, flash, redirect, url_for, session
import uuid 
from welpurse.routes import app_routes, calendar
from welpurse.forms.members import RegistrationForm, LoginForm
import requests
from flask_jwt_extended import current_user, jwt_required
from welpurse.utils import is_logged_in

@app_routes.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register_member():
    reg_url = 'http://127.0.0.1:5001/api/v1/members'
    form = RegistrationForm()
    title = 'Register'
    if isLogedin():
       return redirect(url_for('app_routes.dashboard'))
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'email': form.email.data,
            'password': form.password.data
        }
        res = requests.post(reg_url, json=data)  # Use json parameter here

        if res.status_code == 201:  # Check if the request was successful
            member_data = res.json()  # Access the JSON response data
            flash(f'Account created for {member_data.get("name")}!', 'success')
            return redirect(url_for('app_routes.login'))
        else:
            flash('An error occurred during registration.', 'danger')
    return render_template('register.html', title=title, form=form)

@app_routes.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    url = 'http://127.0.0.1:5001/auth/login'
    form = LoginForm()
    title = 'Login'

    if is_logged_in():
       return redirect(url_for('app_routes.dashboard'))

    if form.validate_on_submit():
        data = {
            'email': form.email.data,
            'password': form.password.data,
            'remember': form.remember.data,
        }
        res = requests.post(url, json=data)
        
        if res.status_code == 200:
            cookies = res.cookies
            # To get a dictionary of cookies
            cookies_dict = cookies.get_dict()
            token = cookies_dict.get('access_token_cookie')
            csrf_token = cookies_dict.get('csrf_access_token')
            session['access_token_cookie'] = token
            session['csrf_access_token'] = csrf_token
            # print("CSRF", csrf_token)
            flash('You have been logged in!', 'success')
            return redirect(url_for('app_routes.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title=title, form=form)

@app_routes.route('/logout', strict_slashes=False, methods=['GET', 'POST'])
def logout():
    url = 'http://127.0.0.1:5001/auth/login'
    res = requests.delete(url=url)

@app_routes.route('/creategroup', strict_slashes=False)
def crete_group():
    title = 'Create Group'
    amount_contributed = 70000
    target = 200000
    progress= (  amount_contributed  / target) * 100
    print("RequestsCookieJar",progress)
    return render_template('creategroup.html',
                           calendar = calendar,
                           title=title,
                           total=amount_contributed,
                           progress=progress,
                           cache_id=uuid.uuid4())

@app_routes.route('/logout', strict_slashes=False)
def logout_route():
    logout()
    flash('You have been logged out!', 'success')
    return redirect(url_for('app_routes.login'))