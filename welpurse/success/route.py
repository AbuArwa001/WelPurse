from flask import render_template, redirect, url_for, flash
import uuid
from welpurse.create_group.form import WelfareGroupForm
from welpurse.utils import login_required
from welpurse.utils import is_logged_in
import requests
from flask import Blueprint

success = Blueprint("success", "__name__")
@success.route(
    "/success-one", methods=["GET", "POST"], strict_slashes=False
)
def success_one():
    title = "Success"
    return render_template("success.html", title=title)


@success.route("/success")
def success_flash():
    flash("Operation was successful!", "success")
    return redirect(url_for("index"))


@success.route("/failure")
def failure():
    flash("Operation failed. Please try again.", "danger")
    return redirect(url_for("index"))
