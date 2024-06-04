
from flask import render_template,redirect, url_for, flash, session
import uuid 
from welpurse.forms.event import EventForm
from welpurse.utils import login_required
from welpurse.routes import app_routes
import requests
import logging
from welpurse.utils import get_current_user
from welpurse.routes.helper_funtions import fetch_welfares, fetch_a_member, start_donation
# Set up basic logging
logging.basicConfig(level=logging.INFO)
from flask import render_template, session, redirect, url_for
from welpurse.routes import app_routes
from welpurse.forms.donation_req import DonationRequestForm


# @login_required 
@app_routes.route('/donation_request', methods=['GET', 'POST'])
def donation_request():
    current_user = get_current_user()
    title = "Donation Request"
    form = DonationRequestForm()

    return render_template('donation.html',

                           current_user=current_user,
                           title=title,
                           form=form)

@app_routes.route('/donations', methods=['GET', 'POST'])
@login_required
def donation_request_view():
    current_user = get_current_user()
    title = "Donation Request View"
    form = DonationRequestForm()
    form_event = EventForm()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    welfares = fetch_welfares(headers=headers).get('data')
    member = fetch_a_member(headers=headers, member_id=current_user.get('id'))

    if form_event.validate_on_submit():
        event_url = "http://127.0.0.1:5001/api/v1/events/"
        # print(form.target_amount.data)
        data = {
            "description": form_event.donation_purpose.data,
            "end_date": form_event.end_date.data.strftime('%Y-%m-%d %H:%M:%S'),
            "event_date": form_event.event_date.data.strftime('%Y-%m-%d %H:%M:%S'),
            "start_date": form_event.start_date.data.strftime('%Y-%m-%d %H:%M:%S'),
            "title": form_event.title.data,
            "status": "ongoing",
            "target_amount": float(form_event.target_amount.data),
            "welfare_id": form_event.welfare_id.data
        }
        try:
            res = requests.post(url=event_url, headers=headers, json=data)
            print(res)
            if res.status_code == 201:
                print("req id", form_event.request_id.data)
                if start_donation(headers=headers, request_id=form.request_id.data):
                    flash("Data passed successfully", "success")
                    return redirect(url_for('app_routes.donation_request_view'))
        except requests.exceptions.RequestException as e:
            flash(f"Error creating event: {e}", 'danger')
    else:
        # Print form errors for debugging
        print("Form errors:", form_event.errors)
    return render_template('donation_req_view.html',
                           form_event=form_event,
                           member=member,
                           welfares=welfares,
                           current_user=current_user,
                           title=title,
                           form=form)


@app_routes.route('/donations/approve/<request_id>', methods=['POST'])
@login_required
def approve_donation(request_id):
    # The URL to the API endpoint that handles the approval of donation requests
    url = f"http://127.0.0.1:5001/api/v1/donation-requests/{request_id}/approve"
    # Headers with the authorization token retrieved from the session
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    # Making a PUT request to the API endpoint with the necessary headers
    res = requests.put(url, headers=headers)
    # Checking if the response status code is 200 (OK)
    if res.status_code == 200:
        # If the request was successful, display a success message
        flash('Successfully Approved', 'success')
    else:
        # If the request failed, display an error message
        flash('Problem Occurred please try again', 'danger')
    # Redirecting to the list of donation requests
    return redirect(url_for('app_routes.donation_request_list'))


# @app_routes.route('/donations/approve/<request_id>', methods=['POST'])
# @login_required
# def approve_donation(request_id):
#     url = f"http://127.0.0.1:5001/api/v1/donation-requests/{request_id}/approve"
#     headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
#     res = requests.put(url, headers)
#     print(res)
#     print(res.json())
#     if res.status_code == 200:
#         flash('Successfully Approve', 'success')
#     else:
#         flash('Problem Occurred please try again', 'danger')
#     return redirect(url_for('app_routes.donation_request_list')) 

@app_routes.route('/donations/reject/<request_id>', methods=['POST'])
@login_required
def reject_donation(request_id):
    url = f"http://127.0.0.1:5001/api/v1/donation-requests/{request_id}/reject"
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    res = requests.put(url, headers)
    if res.status_code == 200:
        flash('Successfully rejected', 'success')
    else:
        flash('Problem Occurred please try again', 'danger')
    return redirect(url_for('app_routes.donation_request_list')) 


@app_routes.route('/donation_list', methods=['GET', 'POST'])
@login_required
def donation_request_list():
    current_user = get_current_user()
    title = "Donation Request List"
    form = DonationRequestForm()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    welfares = fetch_welfares(headers=headers).get('data')
    member = fetch_a_member(headers=headers, member_id=current_user.get('id'))
    print(current_user)
    return render_template('donation_req_list.html',
                           member=member,
                           welfares=welfares,
                           current_user=current_user,
                           title=title,
                           form=form)