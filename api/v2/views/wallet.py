#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse_v2.models import storage
from welpurse_v2.models.wallet import Wallet
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from intasend import APIService
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import os

token = os.getenv("TOKEN")
publishable_key = os.getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)


@app_views.route("/wallets", methods=["GET"], strict_slashes=False)
def get_wallets():
    """Get all Wallets"""
    all_wallets = {}
    all_wallets = storage.all("Wallet")

    wallets = []
    for wallet in all_wallets.values():
        wallets.append(wallet.to_dict())
    res = jsonify(wallets)
    return make_response(res, 200)


@app_views.route("/wallets/<wallet_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user/post_member.yml", methods=["POST"])
def get_one_wallet(wallet_id):
    """
    GET ONE WALLET a user
    """
    wallet = storage.get(Wallet, wallet_id)
    if not wallet:
        abort(404)
    res = jsonify(wallet.to_dict())
    return make_response(res, 200)


@app_views.route(
    "/wallets/<wallet_id>", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/user/post_member.yml", methods=["POST"])
def post_wallet():
    """
    Creates a WALLLET
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "email" not in request.get_json():
        abort(400, description="Missing email")
    if "password" not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = Member(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/wallets/<wallet_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/welfare/update_wallet.yml", methods=["PUT"])
def update_wallet(wallet_id):
    """
    Updates a Wallet
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    wallet = storage.get(Wallet, wallet_id)
    if not wallet:
        abort(404)

    ignore = ["id", "created_at", "updated_at"]
    wallet_dict = wallet.__dict__

    for key, value in data.items():
        if key not in ignore:
            setattr(wallet, key, value)

    storage.save()
    return make_response(jsonify(wallet.to_dict()), 200)
