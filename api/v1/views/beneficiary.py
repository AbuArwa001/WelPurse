#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Member
from welpurse.models.beneficiary import Beneficiary
from welpurse.models.dependent import Dependent
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
intasend.http_client.request = lambda *args, **kwargs: requests.request(*args, timeout=10, **kwargs)

@app_views.route('/beneficiaries', methods=['GET'], strict_slashes=False)
def get_beneficiaries():
    """ Get all Beneficiaries """
    all_beneficiaries = {}
    all_beneficiaries = storage.all(Beneficiary)
    print(all_beneficiaries)
    beneficiaries = []
    for beneficiary in all_beneficiaries.values():
        beneficiaries.append(beneficiary.to_dict())
    res = jsonify(beneficiaries)
    return make_response(res, 200)

@app_views.route('/beneficiaries/<beneficiary_id>', methods=['GET'], strict_slashes=False)
def get_beneficiary(beneficiary_id):
    """ Get One Beneficiaries """
    beneficiary = storage.get(Beneficiary, beneficiary_id)
    res = jsonify(beneficiary.to_dict())
    return make_response(res, 200)

@app_views.route('/beneficiaries', methods=['POST'], strict_slashes=False)
def create_beneficiary():
    """
    Creates a Beneficiary. Expects JSON input with the structure of the Beneficiary model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ['name', 'relation', 'member_id', 'dependent_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Fetch the dependent
    dependent = storage.get(Dependent, data['dependent_id'])
    if not dependent:
        abort(404, description="Dependent not found")

    # Check the status of the dependent
    if dependent.status == 'inactive':
        abort(400, description="Dependent already deceased")
    else:
        dependent.status = 'inactive'

    # Create the Beneficiary instance
    instance = Beneficiary(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/beneficiaries/<beneficiary_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/beneficiary/update_beneficiary.yml', methods=['PUT'])
def update_beneficiary(beneficiary_id):
    """
    Updates a State
    """
    beneficiary = storage.get(Beneficiary, beneficiary_id)
    print(beneficiary)
    if not beneficiary:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(beneficiary, key, value)
    storage.save()
    return make_response(jsonify(beneficiary.to_dict()), 200)

@app_views.route('/beneficiaries/<beneficiary_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/beneficiary/delete_beneficiary.yml', methods=['PUT'])
def delete_beneficiary(beneficiary_id):
    """
    Updates a State
    """
    beneficiary = storage.get(Beneficiary, beneficiary_id)
    if not beneficiary:
        abort(404)

    storage.delete(beneficiary)
    storage.save()
    return make_response(jsonify({}), 204)
