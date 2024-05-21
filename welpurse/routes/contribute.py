#welpurese/routes/main_routess.py
from flask import render_template,redirect, url_for
import uuid 
# from welpurse import calendar
from welpurse.utils import login_required
from welpurse.routes import app_routes
from welpurse import jwt
from flask_jwt_extended import jwt_required, current_user, get_current_user

@app_routes.route('/contributions', methods=['GET', 'POST'],strict_slashes=False)
def contribute():
    return render_template('contribute.html', title='Contribute')