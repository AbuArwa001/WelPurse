
from flask import render_template,redirect, url_for, request, session
import uuid 
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required
from welpurse.routes import app_routes
from welpurse.utils import is_logged_in
import requests
from datetime import datetime, timedelta
import logging
# Set up basic logging
logging.basicConfig(level=logging.INFO)
from flask import render_template, session, redirect, url_for
from welpurse.routes import app_routes
from welpurse.forms.event import EventForm


# @login_required 
@app_routes.route('/events', methods=['GET', 'POST'])
def events():
    title = "Event Requests"
    form = EventForm()
    return render_template('event_list.html',
                           title=title,
                           form=form)

@app_routes.route('/events_view', methods=['GET', 'POST'])
def events_view():
    title = "View Event"
    form = EventForm()
    return render_template('event_view.html',
                           title=title,
                           form=form)

@app_routes.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # Process the form data as needed
        return redirect(url_for('success'))

    if request.method == 'POST':
        welfare_group_name = request.form.get('welfare_group_name')
        amount_requested = request.form.get('amount_requested')
        donation_purpose = request.form.get('donation_purpose')
        current_date = datetime.now()
        start_date = datetime.now()
        end_date = (datetime.now() + timedelta(days=7)) 
         # Example: End date one week later

        form.welfare_group_name.data = welfare_group_name
        form.amount_requested.data = amount_requested
        form.donation_purpose.data = donation_purpose
        form.event_date.data = current_date
        form.start_date.data = start_date
        form.end_date.data = end_date

    return render_template('create_event.html', form=form)
