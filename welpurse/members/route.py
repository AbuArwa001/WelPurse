# welpurse/routes/member_routes.py
from flask import render_template, flash, redirect, url_for, session
import uuid
from welpurse.members.form import RegistrationForm, LoginForm
import requests
from flask_jwt_extended import current_user, jwt_required
from welpurse.utils import is_logged_in, get_current_user, login_required
from flask import Blueprint

members = Blueprint("members", __name__)
@members.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register_member():
    reg_url = "http://127.0.0.1:5001/api/v1/members"
    form = RegistrationForm()
    title = "Register"
    if is_logged_in():
        return redirect(url_for("members.dashboard"))
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        res = requests.post(reg_url, json=data)  # Use json parameter here

        if res.status_code == 201:  # Check if the request was successful
            member_data = res.json()  # Access the JSON response data
            flash(f'Account created for {member_data.get("name")}!', "success")
            return redirect(url_for("members.login"))
        else:
            flash("An error occurred during registration.", "danger")
    return render_template("register.html", title=title, form=form)


# members.py
@members.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    url = "http://127.0.0.1:5001/auth/login"
    form = LoginForm()
    title = "Login"

    if 'access_token' in session:
        return redirect(url_for("members.dashboard"))

    if form.validate_on_submit():
        data = {
            "email": form.email.data,
            "password": form.password.data,
        }
        try:
            res = requests.post(url, json=data)
            # print("RESP_LOGIN", res.json())
            if res.status_code == 200:
                access_token = res.json().get('access_token')
                refresh_token = res.json().get('refresh_token')
                session['access_token'] = access_token
                session['refresh_token'] = refresh_token
                flash("You have been logged in!", "success")
                # print("SESSION", session.get('access_token'))
                return redirect(url_for("main.dashboard"))
            else:
                flash("Login Unsuccessful. Please check email and password", "danger")
        except Exception as e:
            flash("An error occurred during login. Please try again later.", "danger")
            print(f"Error during login request: {e}")

    return render_template("login.html", title=title, form=form)


@members.route("/logout", strict_slashes=False, methods=["GET", "POST"])
@login_required
def logout():
    url = "http://127.0.0.1:5001/auth/logout/"
    headers = {"Authorization": f"Bearer {session.get('access_token')}"}
    res = requests.post(url=url, headers=headers)
    if res.status_code == 200:
        session.pop('access_token', None)
        session.pop("refresh_token", None)
        flash("You have been logged out!", "success")
    else:
        flash("Logout failed.", "danger")
        
    return redirect(url_for("members.login"))

@members.route("/profile", strict_slashes=False, methods=["GET", "POST"])
@login_required
def profile():
    title = "Profile"
    current_user = get_current_user()

    return render_template(
        "profile.html", current_user=current_user, title=title
    )

@members.route("/settings", strict_slashes=False, methods=["GET", "POST"])
@login_required
def settings():
    title = "Settings"
    current_user = get_current_user()

    return render_template(
        "settings.html", current_user=current_user, title=title
    )