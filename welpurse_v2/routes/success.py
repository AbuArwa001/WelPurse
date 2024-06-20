from flask import render_template, redirect, url_for, flash
import uuid
from welpurse_v2.forms.creategroup import WelfareGroupForm
from welpurse_v2.utils import login_required
from welpurse_v2.routes import app_routes
from welpurse_v2.utils import is_logged_in
import requests


@app_routes.route(
    "/success-one", methods=["GET", "POST"], strict_slashes=False
)
def success_one():
    title = "Success"
    return render_template("success.html", title=title)


@app_routes.route("/success")
def success():
    flash("Operation was successful!", "success")
    return redirect(url_for("index"))


@app_routes.route("/failure")
def failure():
    flash("Operation failed. Please try again.", "danger")
    return redirect(url_for("index"))
