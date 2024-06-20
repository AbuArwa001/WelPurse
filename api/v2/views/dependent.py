#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse_v2.models import storage
from welpurse_v2.models.member import Member

# from welpurse_v2.models.dependent import Dependent
from welpurse_v2.models.dependent import Dependent
from flask import abort, jsonify, make_response, request, Response
from flasgger.utils import swag_from
from intasend import APIService
import intasend
from intasend.exceptions import IntaSendBadRequest
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import os
import logging
import json
import requests

# Set up basic logging
logging.basicConfig(level=logging.INFO)

token = os.getenv("TOKEN")
publishable_key = os.getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)
# Set a timeout globally if possible (this is hypothetical and depends on the IntaSend library's implementation)
intasend.http_client = requests.Session()
intasend.http_client.request = lambda *args, **kwargs: requests.request(
    *args, timeout=10, **kwargs
)


@app_views.route("/dependents", methods=["GET"], strict_slashes=False)
def get_dependents():
    """Get all Beneficiaries"""
    all_dependents = {}
    all_dependents = storage.all(Dependent)
    dependents = []
    for dependent in all_dependents.values():
        dependents.append(dependent.to_dict())
    res = jsonify(dependents)
    return make_response(res, 200)


@app_views.route(
    "/dependents/<dependent_id>", methods=["GET"], strict_slashes=False
)
def get_dependent(dependent_id):
    """Get One Beneficiaries"""
    dependent = storage.get(Dependent, dependent_id)
    if not dependent:
        abort(404)
    res = jsonify(dependent.to_dict())
    return make_response(res, 200)


@app_views.route("/dependents", methods=["POST"], strict_slashes=False)
def create_dependent():
    """
    Creates a Dependent. Expects JSON input with the structure of the Dependent model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ["name", "relation", "member_id"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the Dependent instance
    instance = Dependent(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/dependents/<dependent_id>", methods=["PUT"], strict_slashes=False
)
@swag_from("documentation/dependent/update_dependent.yml", methods=["PUT"])
def update_dependent(dependent_id):
    """
    Updates a State
    """
    dependent = storage.get(Dependent, dependent_id)
    if not dependent:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at", "status", "member_id"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(dependent, key, value)
    storage.save()
    return make_response(jsonify(dependent.to_dict()), 200)


@app_views.route(
    "/dependents/<dependent_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/dependent/delete_dependent.yml", methods=["DELETE"])
def delete_dependent(dependent_id):
    """
    Updates a State
    """
    dependent = storage.get(Dependent, dependent_id)
    if not dependent:
        abort(404)

    storage.delete(dependent)
    storage.save()
    return make_response(jsonify({}), 204)
