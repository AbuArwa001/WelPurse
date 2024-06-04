
from flask import render_template,redirect, url_for, flash, session
import uuid 
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required
from welpurse.routes import app_routes
from welpurse.utils import is_logged_in
import requests
import logging
# Set up basic logging
logging.basicConfig(level=logging.INFO)
@app_routes.route('/create_group', methods=['GET', 'POST'])
@login_required 
def create_welfare_group():
    url = 'http://127.0.0.1:5001/api/v1/welfares'
    title = 'Create Group'
    if not is_logged_in():
       return redirect(url_for('app_routes.login'))
    form = WelfareGroupForm()
    # searchable_bool = form.searchable.data == 'True'
    # special_events_bool = form.special_events.data == 'True'
    if form.validate_on_submit():
        data =     {
                "administrator": form.administrator.data,
                "chairperson": form.chairperson.data,
                "contribution_frequency": form.contribution_frequency.data,
                "contribution_modes": form.contribution_modes.data,

                "description": form.description.data,
                "eligibility_requirements": form.eligibility_requirements.data,
                "group_visibility": "Public",
                "membership_approval": form.membership_approval.data,
                "min_contribution": form.min_contribution.data,
                "name": form.welfare_name.data,
                "notification_preferences": form.notification_preferences.data,
                "preferred_communication_channel": form.preferred_communication_channel.data,
                "purpose": form.purpose.data,
                "role_descriptions": {
                    "chairperson": form.role_description_chairperson.data,
                    "treasurer": form.role_description_treasurer.data,
                    "secretary": form.role_description_secretary.data,
                    "vice_chairperson": form.role_description_vice_chair.data,
                    "youth_rep": form.role_description_youth_rep.data
                },
                "searchable": form.searchable.data,
                "secretary": form.secretary.data,
                "special_events": form.special_events.data,
                "treasurer": form.treasurer.data,
                "vice_chairperson": form.vice_chairperson.data,
                "youth_rep": form.youth_rep.data
            }

        headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
        res = requests.post(url=url, headers=headers, json=data)
        logging.info("STATUS CODE: %s", res.status_code)
        if res.status_code == 201:  # Check if the request was successful
            welfare_data = res.json()  # Access the JSON response data
            logging.info("WELFARE DATA %s", welfare_data)
            flash("Succesfuly created a group", "success")
            return redirect (url_for('app_routes.home'))
        logging.error("ERROR OF CREATION %s", res)
    return render_template('creategroup.html', form=form, title=title)