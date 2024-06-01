
from flask import render_template, redirect, url_for, request, session, jsonify, current_app
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required, is_logged_in
from welpurse.routes import app_routes
from welpurse.forms.event import EventForm
from welpurse.forms.contribute import ContributionForm
from os import getenv
from intasend import APIService
from intasend.exceptions import IntaSendBadRequest
import httpx
from datetime import datetime, timedelta
import logging
import asyncio
from asgiref.sync import async_to_sync

# Set up basic logging
logging.basicConfig(level=logging.INFO)

token = getenv("TOKEN")
publishable_key = getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)


@app_routes.route('/events', methods=['GET', 'POST'])
def events():
    from welpurse.payments import initiate_payment, sync_wait_for_payment_completion
    title = "Event Requests"
    url = "http://127.0.0.1:5001/api/v1/events/"
    form = EventForm()
    form_cont = ContributionForm()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}

    async def fetch_events():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_events)()

    if req.status_code == 200:
        events = req.json()
    else:
        events = {}

    if form_cont.validate_on_submit():
        welfare_id = form_cont.welfare_id.data
        welfare = f"http://127.0.0.1:5001/api/v1/welfares/{welfare_id}"
        
        async def fetch_welfare():
            async with httpx.AsyncClient() as client:
                req = await client.get(url=welfare, headers=headers)
            return req

        req = async_to_sync(fetch_welfare)()

        wallet_id = None
        if req.status_code == 200:
            welf = req.json().get('wallet')
        else:
            events = {}
        wallet_id = welf.get('wallet_id')
        amount = form_cont.amount.data
        email = "khalfanathman12@gmail.com"
        phone = form_cont.mpesa_number.data
        try:
            response = initiate_payment(service, wallet_id, email, phone, amount)
            invoice_id = response['invoice']['invoice_id']

            final_state = None
            if invoice_id:
                task = sync_wait_for_payment_completion.apply_async(args=[invoice_id])
                while True:
                    if task.ready():
                        final_state = task.get()
                        break
                    async_to_sync(asyncio.sleep)(1)
            else:
                print("Invoice ID is None")

            if final_state == 'COMPLETE':
                print("Payment has been processed successfully.")
            elif final_state == 'FAILED':
                print("Payment has failed.")
            else:
                print(f"Unexpected payment status: {final_state}")
        except IntaSendBadRequest as e:
            logging.info("ERROR_INFO_KHALFAN  %s", e)
            return render_template('event_list.html',
                                   title=title,
                                   form=form,
                                   events=events,
                                   form_cont=form_cont)
        finally:
            logging.info(form_cont.welfare_id.data)

        if final_state in 'COMPLETE':
            return redirect(url_for('app_routes.success'))

    return render_template('event_list.html',
                           title=title,
                           form=form,
                           events=events,
                           form_cont=form_cont)

@app_routes.route('/events_view', methods=['GET', 'POST'])
async def events_view():
    title = "View Event"
    form = EventForm()
    return render_template('event_view.html',
                           title=title,
                           form=form)

@app_routes.route('/create_event', methods=['GET', 'POST'])
async def create_event():
    form = EventForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))

    if request.method == 'POST':
        welfare_group_name = request.form.get('welfare_group_name')
        amount_requested = request.form.get('amount_requested')
        donation_purpose = request.form.get('donation_purpose')
        current_date = datetime.now()
        start_date = datetime.now()
        end_date = (datetime.now() + timedelta(days=7))  # Example: End date one week later

        form.welfare_group_name.data = welfare_group_name
        form.amount_requested.data = amount_requested
        form.donation_purpose.data = donation_purpose
        form.event_date.data = current_date
        form.start_date.data = start_date
        form.end_date.data = end_date

    return render_template('create_event.html', form=form)
