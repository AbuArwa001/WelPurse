
from flask import render_template,redirect, url_for, request, session
import uuid 
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required
from welpurse.routes import app_routes
from welpurse.utils import is_logged_in
import requests



@app_routes.route('/success', methods=['GET', 'POST'],strict_slashes=False)
def success():
    title = "Success"
    return render_template('success.html', title=title)