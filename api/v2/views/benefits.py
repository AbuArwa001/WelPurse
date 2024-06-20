#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse_v2.models import storage
from welpurse_v2.models.member import Member

# from welpurse_v2.models.benefit import Benefit
from welpurse_v2.models.benefit import Benefit
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)


@app_views.route("/benefits", methods=["GET"], strict_slashes=False)
def get_benefits():
    """Get all Beneficiaries"""
    all_benefits = {}
    all_benefits = storage.all(Benefit)
    benefits = []
    for benefit in all_benefits.values():
        benefits.append(benefit.to_dict())
    res = jsonify(benefits)
    return make_response(res, 200)


@app_views.route(
    "/benefits/<benefit_id>", methods=["GET"], strict_slashes=False
)
def get_benefit(benefit_id):
    """Get One Beneficiaries"""
    benefit = storage.get(Benefit, benefit_id)
    if not benefit:
        abort(404)
    res = jsonify(benefit.to_dict())
    return make_response(res, 200)


@app_views.route("/benefits", methods=["POST"], strict_slashes=False)
def create_benefit():
    """
    Creates a Benefit. Expects JSON input with the structure of the Benefit model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ["amount", "date_received", "member_id"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the Benefit instance
    instance = Benefit(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/benefits/<benefit_id>", methods=["PUT"], strict_slashes=False
)
@swag_from("documentation/benefit/update_benefit.yml", methods=["PUT"])
def update_benefit(benefit_id):
    """
    Updates a State
    """
    benefit = storage.get(Benefit, benefit_id)
    if not benefit:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at", "status", "member_id"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(benefit, key, value)
    storage.save()
    return make_response(jsonify(benefit.to_dict()), 200)


@app_views.route(
    "/benefits/<benefit_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/benefit/delete_benefit.yml", methods=["DELETE"])
def delete_benefit(benefit_id):
    """
    Updates a State
    """
    benefit = storage.get(Benefit, benefit_id)
    if not benefit:
        abort(404)

    storage.delete(benefit)
    storage.save()
    return make_response(jsonify({}), 204)
