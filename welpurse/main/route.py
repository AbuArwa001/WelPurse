from flask import render_template, redirect, url_for, flash, session, Blueprint
import uuid
from welpurse.utils import login_required
import requests
from welpurse.contribute.form import ContributionForm
from welpurse.donation_req.form import DonationRequestForm
from datetime import datetime, timedelta
import asyncio
from welpurse.utils import get_current_user

from welpurse.helper_functions.utils import (
    fetch_events,
    fetch_a_member,
    fetch_an_event,
    update_database,
    fetch_intasend_wallet,
    fetch_wallet,
    fetch_welfares,
    fetch_wallet_id,
    fetch_a_welfare,
    process_payment,
    async_events_view,
    update_wallet,
)
main = Blueprint("main", __name__)

@main.route("/", strict_slashes=False)
def landingpage():
    """Goes to landing page"""
    return render_template("landingpage.html")


# @login_required
@main.route("/home", strict_slashes=False)
def home():
    """Page displaying welfares"""
    # Check if the session variables exist
    current_user = get_current_user()

    headers = {"Authorization": f"Bearer {session.get('access_token')}"}
    member_id = current_user.get("id") if current_user else None
    member = fetch_a_member(headers=headers, member_id=member_id)
    welfares = fetch_welfares(headers=headers).get("data")
    return render_template(
        "index.html",
        cache_id=uuid.uuid4(),
        welfares=welfares,
        current_user=current_user,
        member_id=member_id,
        member=member,
    )


@main.route("/dashboard", strict_slashes=False)
@login_required  # Use custom login_required decorator
def dashboard():
    current_user = get_current_user()
    title = "dashboard"
    amount_contributed = 70000
    target = 200000
    progress = (amount_contributed / target) * 100
    accessToken = session.get('access_token')
    headers = {"Authorization": f"Bearer {accessToken}"}
    # response = requests.get('http://127.0.0.1:5001/api/v1/events/')

    events = fetch_events(headers)

    if events:

        # Format the data for FullCalendar
        formatted_events = []
        for event in events:
            formatted_events.append(
                {
                    "id": event["id"],
                    "title": event["title"],
                    "start_event": event["start_date"],
                    "end_event": event["end_date"],
                }
            )
    # Render the dashboard page if authenticated
    # print("ACCESS TOKEN:", accessToken)
    return render_template(
        "__main.html",
        accessToken=accessToken,
        current_user=current_user,
        calendar=formatted_events,
        title=title,
        total=amount_contributed,
        progress=progress,
        cache_id=uuid.uuid4(),
    )


@main.route(
    "/group_dash/<welfare_id>", methods=["GET", "POST"], strict_slashes=False
)
@login_required  # Use custom login_required decorator
def group_dash(welfare_id):
    current_user = get_current_user()

    title = "Welfare"
    amount_contributed = 70000
    target = 200000
    progress = (amount_contributed / target) * 100
    form = ContributionForm()
    form_req = DonationRequestForm()
    headers = {"Authorization": f"Bearer {session.get('access_token')}"}
    current_user = get_current_user()
    print("CURRENT USER", current_user)
    welf = fetch_a_welfare(headers, welfare_id)

    # Run the asynchronous tasks synchronously
    wallet = asyncio.run(
        fetch_intasend_wallet(headers, welf.get("wallet")["wallet_id"])
    )
    updated_wallet = asyncio.run(
        update_wallet(headers, welf.get("wallet")["id"], wallet)
    )

    member_count = welf.get("member_count")
    events = fetch_events(headers)
    formatted_events = []
    if events:
        # Format the data for FullCalendar
        for event in events:
            if event.get("welfare_id") == welfare_id:
                # if event.get('welfare_id'):
                formatted_events.append(
                    {
                        "id": event["id"],
                        "title": event["title"],
                        "start_event": event["start_date"],
                        "end_event": event["end_date"],
                    }
                )
    form.welfare_id = welfare_id
    # form.event_id =
    if form.validate_on_submit():
        welfare = f"http://127.0.0.1:5001/api/v1/welfares/{welfare_id}"
        wallet = fetch_wallet_id(welfare, headers)

        if wallet:
            amount = form.amount.data
            email = current_user.get("email")
            phone = form.mpesa_number.data
            event_id = form.event_id.data
            if process_payment(
                current_user,
                wallet,
                email,
                phone,
                amount,
                event_id,
                "1",
                "monthly",
            ):
                flash("Contributed successfully!", "success")
            else:
                flash("Contribution failed! try Again", "danger")
    if form_req.validate_on_submit():
        req_url = f"http://127.0.0.1:5001/api/v1/donation-request/"
        data = {
            "reason": form_req.reason.data,
            "amount_requested": form_req.amount_requested.data,
            "member_id": form_req.member_id.data,
            "welfare_id": form_req.welfare_id.data,
        }
        res = requests.post(req_url, headers=headers, json=data)
        if res.status_code != 201:
            flash("Request Not completed please try Again Later", "danger")
        else:
            flash("Request Sent Succesfully", "success")
    # Render the dashboard page if authenticated
    return render_template(
        "group_dash.html",
        form=form,
        form_req=form_req,
        welfare=welf,
        current_user=current_user,
        updated_wallet=updated_wallet,
        member_count=member_count,
        calendar=formatted_events,
        title=title,
        total=amount_contributed,
        progress=progress,
        cache_id=uuid.uuid4(),
    )