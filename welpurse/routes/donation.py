
from flask import render_template,redirect, url_for, request, session
import uuid 
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required
from welpurse.routes import app_routes
from welpurse.utils import is_logged_in
import requests
import logging
# Set up basic logging
logging.basicConfig(level=logging.INFO)
from flask import render_template, session, redirect, url_for
from welpurse.routes import app_routes
from welpurse.forms.donation_req import DonationRequestForm


# @login_required 
@app_routes.route('/donation_request', methods=['GET', 'POST'])
def donation_request():
    title = "Donation Request"
    form = DonationRequestForm()
    return render_template('donation.html',
                           title=title,
                           form=form)

@app_routes.route('/donations', methods=['GET', 'POST'])
def donation_request_view():
    title = "Donation Request View"
    form = DonationRequestForm()
    return render_template('donation_req.html',
                           title=title,
                           form=form)