#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Member

# from welpurse.models.contribution import Contribution
from welpurse.models.contribution import Contribution
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from intasend.exceptions import IntaSendBadRequest
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)


@app_views.route("/contributions", methods=["GET"], strict_slashes=False)
def get_contributions():
    """Get all Beneficiaries"""
    all_contributions = {}
    all_contributions = storage.all(Contribution)
    contributions = []
    for contribution in all_contributions.values():
        contributions.append(contribution.to_dict())
    res = jsonify(contributions)
    return make_response(res, 200)


@app_views.route(
    "/contributions/<contribution_id>", methods=["GET"], strict_slashes=False
)
def get_contribution(contribution_id):
    """Get One Beneficiaries"""
    contribution = storage.get(Contribution, contribution_id)
    if not contribution:
        abort(404)
    res = jsonify(contribution.to_dict())
    return make_response(res, 200)


@app_views.route("/contributions", methods=["POST"], strict_slashes=False)
def create_contribution():
    """
    Creates a Contribution. Expects JSON input with the structure of the Contribution model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ["amount", "date_contributed", "member_id"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the Contribution instance
    instance = Contribution(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/contributions/<contribution_id>", methods=["PUT"], strict_slashes=False
)
@swag_from(
    "documentation/contribution/update_contribution.yml", methods=["PUT"]
)
def update_contribution(contribution_id):
    """
    Updates a State
    """
    contribution = storage.get(Contribution, contribution_id)
    if not contribution:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at", "status", "member_id"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(contribution, key, value)
    storage.save()
    return make_response(jsonify(contribution.to_dict()), 200)


@app_views.route(
    "/contributions/<contribution_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
@swag_from(
    "documentation/contribution/delete_contribution.yml", methods=["DELETE"]
)
def delete_contribution(contribution_id):
    """
    Updates a State
    """
    contribution = storage.get(Contribution, contribution_id)
    if not contribution:
        abort(404)

    storage.delete(contribution)
    storage.save()
    return make_response(jsonify({}), 204)
