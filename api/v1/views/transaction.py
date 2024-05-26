#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Member
# from welpurse.models.transaction import WalletTransaction
from welpurse.models.transaction import WalletTransaction
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from intasend.exceptions import IntaSendBadRequest
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
import logging
# Set up basic logging
logging.basicConfig(level=logging.INFO)

@app_views.route('/transactions', methods=['GET'], strict_slashes=False)
def get_transactions():
    """ Get all Beneficiaries """
    all_transactions = {}
    all_transactions = storage.all(WalletTransaction)
    transactions = []
    for transaction in all_transactions.values():
        transactions.append(transaction.to_dict())
    res = jsonify(transactions)
    return make_response(res, 200)

@app_views.route('/transactions/<transaction_id>', methods=['GET'], strict_slashes=False)
def get_transaction(transaction_id):
    """ Get One Beneficiaries """
    transaction = storage.get(WalletTransaction, transaction_id)
    if not transaction:
        abort(404)
    res = jsonify(transaction.to_dict())
    return make_response(res, 200)

@app_views.route('/transactions', methods=['POST'], strict_slashes=False)
def create_transaction():
    """
    Creates a WalletTransaction. Expects JSON input with the structure of the WalletTransaction model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ['amount', 'transaction_type', 'wallet_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the WalletTransaction instance
    instance = WalletTransaction(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/transactions/<transaction_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/transaction/update_transaction.yml', methods=['PUT'])
def update_transaction(transaction_id):
    """
    Updates a State
    """
    transaction = storage.get(WalletTransaction, transaction_id)
    if not transaction:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'status', "member_id"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(transaction, key, value)
    storage.save()
    return make_response(jsonify(transaction.to_dict()), 200)

@app_views.route('/transactions/<transaction_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/transaction/delete_transaction.yml', methods=['DELETE'])
def delete_transaction(transaction_id):
    """
    Updates a State
    """
    transaction = storage.get(WalletTransaction, transaction_id)
    if not transaction:
        abort(404)

    storage.delete(transaction)
    storage.save()
    return make_response(jsonify({}), 204)
