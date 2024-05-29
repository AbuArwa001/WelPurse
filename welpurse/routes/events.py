
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
@app_routes.route('/events', methods=['GET', 'POST'])
def events():
    title = "Event Requests"
    form = DonationRequestForm()
    return render_template('event_list.html',
                           title=title,
                           form=form)

@app_routes.route('/events_view', methods=['GET', 'POST'])
def events_view():
    title = "View Event"
    form = DonationRequestForm()
    return render_template('event_view.html',
                           title=title,
                           form=form)

@app_routes.route('/create_event', methods=['GET', 'POST'])
def create_event():
    title = "Create Event"
    form = DonationRequestForm()
    return render_template('create_event.html',
                           title=title,
                           form=form)