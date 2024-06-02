import time
import json
from flask import render_template, redirect, url_for, request, session, jsonify, flash
from welpurse.forms.creategroup import WelfareGroupForm
from welpurse.utils import login_required, is_logged_in
from flask_jwt_extended import get_jwt_identity, jwt_required
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
import requests
from asgiref.sync import async_to_sync
from welpurse.utils import login_required, get_current_user

# Set up basic logging
logging.basicConfig(level=logging.INFO)

token = getenv("TOKEN")
publishable_key = getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)


@app_routes.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    title = "Event Requests"
    form = EventForm()
    form_cont = ContributionForm()
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    current_user = get_current_user()
    logging.info("current_user.id == %s", current_user.get('id'))
    events = fetch_events(headers)

    if form_cont.validate_on_submit():
        welfare_id = form_cont.welfare_id.data
        welfare = f"http://127.0.0.1:5001/api/v1/welfares/{welfare_id}"
        wallet = fetch_wallet_id(welfare, headers)

        if wallet:
            amount = form_cont.amount.data
            email = "khalfanathman12@gmail.com"
            phone = form_cont.mpesa_number.data
            event_id = form_cont.event_id.data

            if process_payment(current_user, wallet, email, phone, amount, event_id):
                flash('Payment was successful!', 'success')
                return redirect(url_for('app_routes.events'))

    return render_template('event_list.html', title=title, form=form, events=events, form_cont=form_cont)

def fetch_events(headers):
    url = "http://127.0.0.1:5001/api/v1/events/"
    
    async def fetch_events_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_events_async)()
    return req.json() if req.status_code == 200 else {}

def fetch_wallet_id(welfare_url, headers):
    async def fetch_welfare_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=welfare_url, headers=headers)
        return req

    req = async_to_sync(fetch_welfare_async)()
    if req.status_code == 200:
        welf = req.json().get('wallet')
        return welf if welf else None
    return None

def process_payment(current_user, wallet, email, phone, amount, event_id):
    from welpurse.payments import initiate_payment
    try:
        response = initiate_payment(service, wallet, email, phone, amount)
        invoice_id = response['invoice']['invoice_id']
        if invoice_id:
            final_state = wait_for_payment_completion(invoice_id)
            if final_state == 'COMPLETE':
                if update_database(current_user, wallet, amount, event_id):
                    # flash('Payment was successful!', 'success')
                    print("Payment has been processed successfully.")
                    return True
            elif final_state == 'FAILED':
                flash('Payment was unsuccessful!', 'danger')
                print("Payment has failed.")
            else:
                print(f"Unexpected payment status: {final_state}")
        else:
            print("Invoice ID is None")
    except IntaSendBadRequest as e:
        logging.info("ERROR_INFO_KHALFAN  %s", e)
    return False

def wait_for_payment_completion(invoice_id):
    from welpurse.payments import sync_wait_for_payment_completion
    task = sync_wait_for_payment_completion.apply_async(args=[invoice_id])
    retries = 0
    while True:
        if task.ready():
            return task.get()
        async_to_sync(asyncio.sleep)(2 ** retries)
        retries += 1

def update_database(current_user, wallet, amount, event_id):

    wt_url = "http://127.0.0.1:5001/api/v1/transactions/"
    wallet_id = wallet.get('id')
    wallet_transactions = {
        "wallet_id": wallet_id,
        "amount": amount,
        "transaction_type": "3",
        "date_transaction": datetime.now().date().isoformat() 
    }
    try:
        if not check_wallet_exists(wallet_id):
            flash('Wallet ID does not exist. Operation failed!', 'danger')
            return False
        wt_res = requests.post(wt_url, json=wallet_transactions)
        if wt_res.status_code != 201:
            return False
    except Exception as e:
        flash('Payment was unsuccessful! Please try again later', 'danger')
        print("FAILED", e)
        return False

    trans_type_url = "http://127.0.0.1:5001/api/v1/transactions_ttype/"
    transaction_transaction_type = {
        "transaction_id": wt_res.json().get('id'),
        "type_id": "3"
    }
    try:
        trans_type_res = requests.post(trans_type_url, json=transaction_transaction_type)
        if trans_type_res.status_code != 201:
            flash('Payment was unsuccessful! - transaction, try again', 'danger')
            return False
    except Exception as e:
        flash('Payment was unsuccessful!', 'danger')
        return False
    contr_url = "http://127.0.0.1:5001/api/v1/contributions/"
    contribution = {
        "member_id": current_user.get('id'),
        "amount": amount,
        "contribution_type": "event",
        "event_id": event_id,
        "date_contributed": datetime.now().date().isoformat() ,
    }
    try:
        contr_res = requests.post(contr_url, json=contribution)
        print(contr_res)
        if contr_res.status_code != 201:
            flash('Payment was unsuccessful-contr!, try again', 'danger')
            return False
    except Exception as e:
        flash('Payment was unsuccessful!, try again', 'danger')
        return False

    return True

def check_wallet_exists(wallet_id):
    wallet_url = f"http://127.0.0.1:5001/api/v1/wallets/{wallet_id}"
    try:
        res = requests.get(wallet_url)
        return res.status_code == 200
    except Exception as e:
        print("Error checking wallet existence:", e)
        return False

@app_routes.route('/events_view', methods=['GET', 'POST'])
async def events_view():
    title = "View Event"
    form = EventForm()
    return render_template('event_view.html', title=title, form=form)

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
        end_date = (datetime.now() + timedelta(days=7))

        form.welfare_group_name.data = welfare_group_name
        form.amount_requested.data = amount_requested
        form.donation_purpose.data = donation_purpose
        form.event_date.data = current_date
        form.start_date.data = start_date
        form.end_date.data = end_date

    return render_template('create_event.html', form=form)
