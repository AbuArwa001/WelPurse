
from flask import render_template, redirect, url_for, request, session, flash
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required, is_logged_in
from welpurse.routes import app_routes
from welpurse.forms.event import EventForm
from welpurse.forms.contribute import ContributionForm
from datetime import datetime, timedelta
import asyncio
import logging
import requests
from welpurse.utils import get_current_user
from welpurse.utils import login_required, get_current_user
from .helper_funtions import( fetch_events,
                             fetch_welfares,
                            fetch_wallet_id,
                            process_payment,
                            async_events_view
                            )

# Set up basic logging
logging.basicConfig(level=logging.INFO)


@app_routes.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    current_user = get_current_user()
    title = "Event Requests"
    time = "%Y-%m-%dT%H:%M:%S.%f"
    form = EventForm()
    form_cont = ContributionForm()
    today = datetime.utcnow()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    current_user = get_current_user()
    logging.info("current_user.id == %s", current_user.get('id'))
    all_welfares = fetch_welfares(headers)['data']
    # print(all_welfares)
    all_events = fetch_events(headers)
    if all_events:
        events = [event for event in all_events if datetime.fromisoformat(event['end_date']) >= today]
    else:
       events = []
    if form_cont.validate_on_submit():
        welfare_id = form_cont.welfare_id.data
        welfare = f"http://127.0.0.1:5001/api/v1/welfares/{welfare_id}"
        wallet = fetch_wallet_id(welfare, headers)

        if wallet:
            amount = form_cont.amount.data
            email = "khalfanathman12@gmail.com"
            phone = form_cont.mpesa_number.data
            event_id = form_cont.event_id.data

            if process_payment(current_user, wallet, email, phone, amount, event_id, "3", "event"):
                flash('Payment was successful!', 'success')
                return redirect(url_for('app_routes.events'))

    return render_template('event_list.html',
                           time=time,
                           today=today,
                           datetime=datetime,
                           current_user=current_user,
                           welfares=all_welfares,
                           title=title,
                           form=form,
                           events=events,
                           form_cont=form_cont)

@app_routes.route('/events_view/<welfare_id>/<event_id>/', methods=['GET', 'POST'])
@login_required
def events_view(welfare_id, event_id):
    current_user = get_current_user()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    result = asyncio.run(async_events_view(welfare_id, event_id, headers))

    if "error" in result:
        flash(result["error"], 'danger')
        return redirect(url_for('app_routes.events'))
    
    welfare = result["welfare"]
    event = result["event"]
    updated_wallet = result["updated_wallet"]
    
    title = "View Event"
    form = EventForm()
    return render_template('event_view.html',
                           wallet=updated_wallet,
                           current_user=current_user,
                           welfare=welfare,
                           event=event,
                           title=title,
                           form=form)

@app_routes.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    current_user = get_current_user()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    form = EventForm()

    if form.validate_on_submit():
        event_url = "http://127.0.0.1:5001/api/v1/events/"
        print(form.target_amount.data)
        data = {
            "description": form.donation_purpose.data,
            "end_date": form.end_date.data.strftime('%Y-%m-%d %H:%M:%S'),
            "event_date": form.event_date.data.strftime('%Y-%m-%d %H:%M:%S'),
            "start_date": form.start_date.data.strftime('%Y-%m-%d %H:%M:%S'),
            "title": form.title.data,
            "target_amount": float(form.target_amount.data),
            "welfare_id": form.welfare_id.data
        }
        try:
            res = requests.post(url=event_url, headers=headers, json=data)
            if res.status_code == 200:
                flash("Data passed successfully", "success")
                return redirect(url_for('app_routes.donation_request_view'))
        except requests.exceptions.RequestException as e:
            flash(f"Error creating event: {e}", 'danger')
    else:
        # Print form errors for debugging
        print("Form errors:", form.errors)

    return render_template('create_event.html', 
                           current_user=current_user,
                           form=form)
