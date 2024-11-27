from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.welfare import Welfare
from welpurse.models.member import Member
from welpurse.models.contribution import Contribution
from welpurse.models.donation_request import DonationRequest
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    unset_jwt_cookies,
    set_access_cookies,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flasgger.utils import swag_from
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)


@app_views.route(
    "/donation-request/<welfare_id>", methods=["GET"], strict_slashes=False
)
def get_request_donation(welfare_id):
    welfare = storage.get(Welfare, welfare_id)
    if not welfare:
        abort(404, "Welfare Not Found")
    all_requests = welfare.requests
    # all_requests = welfare.requests
    req_list = [req.to_dict() for req in all_requests]

    return make_response(jsonify(req_list), 200)


# @app_views.route('/donation-request', methods=['POST'], strict_slashes=False)
# @jwt_required()
# def request_donation():
@app_views.route("/donation-request/", methods=["POST"], strict_slashes=False)
def request_donation():
    data = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")

    required_fields = ["reason", "amount_requested", "member_id", "welfare_id"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    welfare = storage.get(Welfare, data["welfare_id"])
    if not welfare:
        abort(404, description="Welfare not found")

    member = storage.get(Member, data["member_id"])
    if not member:
        abort(404, description="Member not found")
    member_list = [member for member in welfare.members]
    print(member_list)
    if member not in welfare.members:
        abort(
            404, description="Member does not belong to the specified welfare"
        )

    instance = DonationRequest(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


# @app_views.route('/donation-requests/<request_id>/approve', methods=['PUT', 'POST'], strict_slashes=False)
# def approve_donation_request(request_id):
@app_views.route(
    "/donation-requests/<request_id>/start",
    methods=["PUT", "POST"],
    strict_slashes=False,
)
# @jwt_required()
def star_donation(request_id):
    print("TRYING START")
    if not user_is_admin():
        abort(403, description="Forbidden")

    donation_request = storage.get(DonationRequest, request_id)
    print("donation req", donation_request)
    if not donation_request:
        abort(404, description="Donation request not found")
    if donation_request.status == "rejected":
        return jsonify(donation_request.to_dict())
    elif donation_request.status == "approved":
        donation_request.status = "ongoing"
        donation_request.save()
        return jsonify(donation_request.to_dict())
    return jsonify(donation_request.to_dict()), 200


# @app_views.route('/donation-requests/<request_id>/approve', methods=['PUT', 'POST'], strict_slashes=False)
# def approve_donation_request(request_id):
# @jwt_required()
@app_views.route(
    "/donation-requests/<request_id>/approve",
    methods=["PUT", "POST"],
    strict_slashes=False,
)
def approve_donation_request(request_id):
    if not user_is_admin():
        abort(403, description="Forbidden")

    donation_request = storage.get(DonationRequest, request_id)
    if not donation_request:
        abort(404, description="Donation request not found")
    if donation_request.status == "rejected":
        return jsonify(donation_request.to_dict())
    elif donation_request.status == "approved":
        return jsonify(donation_request.to_dict())

    donation_request.status = "approved"
    donation_request.save()
    return jsonify(donation_request.to_dict()), 200


@app_views.route(
    "/donation-requests/<request_id>/reject",
    methods=["PUT"],
    strict_slashes=False,
)
# @jwt_required()
def reject_donation_request(request_id):
    if not user_is_admin():
        abort(403, description="Forbidden")

    donation_request = storage.get(DonationRequest, request_id)
    if not donation_request:
        abort(404, description="Donation request not found")
    if donation_request.status == "rejected":
        return jsonify(donation_request.to_dict())
    elif donation_request.status == "approved":
        return jsonify(donation_request.to_dict())

    donation_request.status = "reject"
    donation_request.save()
    return jsonify(donation_request.to_dict()), 200


def user_is_admin():
    current_user = get_jwt_identity()
    member = storage.get(
        Member, current_user
    )  # Adjust according to your user model and storage method
    member_roles = member.roles

    # Now you can iterate over the member_roles list to get each Role object
    for role in member_roles:
        print(role.name)
        if role.name == "administrator":
            return True
    return False
    # return user and user.role == 'administrator'


@app_views.route("/donate/", methods=["POST"], strict_slashes=False)
def donate():
    data = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Required fields for donation
    required_fields = [
        "amount",
        "member_id",
        "welfare_id",
        "contribution_type",
        "wallet_id",
        "email",
        "phone",
    ]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    welfare = storage.get(Welfare, data["welfare_id"])
    if not welfare:
        abort(404, description="Welfare not found")

    member = storage.get(Member, data["member_id"])
    if not member:
        abort(404, description="Member not found")

    if member not in welfare.members:
        abort(
            404, description="Member does not belong to the specified welfare"
        )

    if data["contribution_type"] not in ["monthly", "event"]:
        abort(400, description="Invalid contribution type")

    event_id = data.get("event_id")
    if data["contribution_type"] == "event":
        if not event_id:
            abort(
                400,
                description="Missing event ID for event-specific contribution",
            )
        event = storage.get(Event, event_id)
        if not event or event.welfare_id != data["welfare_id"]:
            abort(404, description="Invalid event ID")

    # Fund the wallet
    amount = data["amount"]
    email = data["email"]
    phone = data["phone"]
    wallet_id = data["wallet_id"]

    response = service.wallets.fund(
        wallet_id=wallet_id,
        email=email,
        phone_number=phone,
        amount=amount,
        currency="KES",
        narrative="Donation",
        mode="MPESA-STK-PUSH",
    )

    if response.get("status") != "success":
        abort(500, description="Failed to fund wallet")

    # Create the contribution
    contribution_data = {
        "member_id": data["member_id"],
        "welfare_id": data["welfare_id"],
        "amount": data["amount"],
        "contribution_type": data["contribution_type"],
        "event_id": event_id if data["contribution_type"] == "event" else None,
    }
    contribution = Contribution(**contribution_data)
    storage.new(contribution)
    storage.save()

    return jsonify(contribution.to_dict()), 201
