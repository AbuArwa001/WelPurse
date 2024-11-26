# welpurese/routes/main_routess.py
from flask import render_template, redirect, url_for, Blueprint
import uuid

# from welpurse import calendar
from welpurse.utils import login_required
# from welpurse.routes import app_routes
from flask_jwt_extended import jwt_required, current_user, get_current_user
from welpurse.contribute.form import ContributionForm

contribute = Blueprint("main", __name__)

@contribute.route("/contribute", methods=["GET", "POST"], strict_slashes=False)
def contribute():
    form = ContributionForm()
    if form.validate_on_submit():

        return redirect(url_for("success.success_route"))

    return render_template("contribute.html", form=form)
