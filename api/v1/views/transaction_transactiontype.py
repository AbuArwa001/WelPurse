#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Member

# from welpurse.models.transactiontype import TransactionTypes
from welpurse.models.transactiontype import TransactionType
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)


@app_views.route(
    "/transaction_transactiontypes/", methods=["GET"], strict_slashes=False
)
def get_transaction_transactiontypes():
    """Get all Beneficiaries"""
    all_transaction_transactiontypes = {}
    all_transaction_transactiontypes = storage.all(TransactionType)
    transaction_transactiontypes = []
    for transactiontype in all_transaction_transactiontypes.values():
        transaction_transactiontypes.append(transactiontype.to_dict())
    res = jsonify(transaction_transactiontypes)
    return make_response(res, 200)


@app_views.route(
    "/transaction_transactiontypes/<transactiontype_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_transactiontype(transactiontype_id):
    """Get One Beneficiaries"""
    transactiontype = storage.get(TransactionType, transactiontype_id)
    if not transactiontype:
        abort(404)
    res = jsonify(transactiontype.to_dict())
    return make_response(res, 200)


@app_views.route(
    "/transaction_transactiontypes/", methods=["POST"], strict_slashes=False
)
def create_transactiontype():
    """
    Creates a TransactionType. Expects JSON input with the structure of the TransactionType model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ["name"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the TransactionType instance
    instance = TransactionType(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/transaction_transactiontypes/<transactiontype_id>",
    methods=["PUT"],
    strict_slashes=False,
)
@swag_from(
    "documentation/transactiontype/update_transactiontype.yml", methods=["PUT"]
)
def update_transactiontype(transactiontype_id):
    """
    Updates a State
    """
    transactiontype = storage.get(TransactionType, transactiontype_id)
    if not transactiontype:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at", "status", "member_id"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(transactiontype, key, value)
    storage.save()
    return make_response(jsonify(transactiontype.to_dict()), 200)


@app_views.route(
    "/transaction_transactiontypes/<transactiontype_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
@swag_from(
    "documentation/transactiontype/delete_transactiontype.yml",
    methods=["DELETE"],
)
def delete_transactiontype(transactiontype_id):
    """
    Updates a State
    """
    transactiontype = storage.get(TransactionType, transactiontype_id)
    if not transactiontype:
        abort(404)

    storage.delete(transactiontype)
    storage.save()
    return make_response(jsonify({}), 204)
