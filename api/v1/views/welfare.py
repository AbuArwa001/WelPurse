#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Welfare
from welpurse.models.wallet import Wallet
from flask import abort, jsonify, make_response, request
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

@app_views.route('/welfares', methods=['GET'], strict_slashes=False)
def get_welfares():
    """ Get all Members """
    all_welfares = {}
    all_welfares = storage.all(Welfare)
    print(all_welfares)
    welfares = []
    for welfare in all_welfares.values():
        welfares.append(welfare.to_dict())
    res = jsonify(welfares)
    return make_response(res, 200)


def create_wallet(label, welfare_id):
    """
    Create a wallet with the specified label and welfare ID.
    """
    try:
        logging.info("Attempting to create wallet with label: %s", label)
        response = service.wallets.create(currency="KES", label=label, can_disburse=True)
        if response.status_code != 200:
            logging.error("Failed to create wallet, status code: %d", response.status_code)
            return None, "Failed to create wallet"
    except IntaSendBadRequest as e:
        try:
            error_data = json.loads(e.args[0])
            logging.error("IntaSendBadRequest error: %s", error_data)
            if 'errors' in error_data and error_data['errors'][0]['code'] == 'invalid_request_data':
                detail = error_data['errors'][0]['detail']
                return 400, f"Invalid request data: {detail}"
        except (json.JSONDecodeError, IndexError, KeyError) as parse_error:
            logging.exception("Error parsing IntaSendBadRequest response: %s", parse_error)
            return 400, "An unexpected error occurred"
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)
        return 400, "An unexpected error occurred"

    return response.json(), None

@app_views.route('/welfares', methods=['POST'], strict_slashes=False)
def create_welfare():
    """
    Creates a Welfare. Expects JSON input with the structure of the Welfare model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ['name', 'description', 'special_events']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Validate 'special_events' as boolean
    if not isinstance(data['special_events'], bool):
        abort(400, description="Invalid data type for special_events. Must be a boolean.")

    # Convert 'contribution_modes' to a JSON string if it exists and is a list
    if 'contribution_modes' in data and isinstance(data['contribution_modes'], list):
        data['contribution_modes'] = json.dumps(data['contribution_modes'])
    elif 'contribution_modes' in data and not isinstance(data['contribution_modes'], list):
        abort(400, description="Invalid data type for contribution_modes. Must be a list.")

    # Create the Welfare instance
    instance = Welfare(**data)
    
    try:
        data , message = create_wallet(instance.name, instance.id)
    except Exception as e:
        abort(400, description=str(e))

    # Save the Welfare instance
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/welfares/<welfare_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/welfare/update_welfare.yml', methods=['PUT'])
def update_welfare(welfare_id):
    """
    Updates a State
    """
    welfare = storage.get(Welfare, welfare_id)
    print(welfare)
    if not welfare:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(welfare, key, value)
    storage.save()
    return make_response(jsonify(welfare.to_dict()), 200)
