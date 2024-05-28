import requests
import json

import requests
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from intasend import APIService
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
from os import getenv

token = getenv("TOKEN") 
publishable_key = getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)


# Retrieve Wallets
@app_views.route('/wallet', methods=['GET'], strict_slashes=False)
def get_wallet():
    response = service.wallets.retrieve()
    # print(response)
        # print(f"Failed to get access token: {response.status_code}")
    return jsonify(response)

@app_views.route('/wallet/<wallets_id>', methods=['GET'], strict_slashes=False)
def get_wallet_by_id(wallets_id):
    response = service.wallets.details(wallets_id)
    # print(response)
        # print(f"Failed to get access token: {response.status_code}")
    return jsonify(response)

# CREATE WALLETS
@app_views.route('/wallets/<label>', methods=['POST'], strict_slashes=False)
def create_wallet(label):
    response = service.wallets.create(currency="KES", label=label, can_disburse=True)
    # print(response)
        # print(f"Failed to get access token: {response.status_code}")
    return jsonify(response)


# WALLET TRANSACTIONS 
@app_views.route('/wallets_transact/<wallet_id>', methods=['GET'], strict_slashes=False)
def wallet_transact(wallet_id):
    response = service.wallets.transactions(wallet_id)
    return jsonify(response)


# FUND WALLET
# Mpesa
@app_views.route('/wallets/<wallet_id>', methods=['POST'], strict_slashes=False)
def fund_wallet_mpesa(wallet_id):
    amount = 1
    email = "khalfanathman12@gmail.com"
    phone = "254740403037"
    response = service.wallets.fund(wallet_id=wallet_id,
                                    email=email, phone_number=phone,
                                amount=amount, currency="KES", narrative="Deposit", 
                                mode="MPESA-STK-PUSH")
    return jsonify(response)

# CHECKOUT
@app_views.route('/wallets/checkout/<wallet_id>', methods=['POST'], strict_slashes=False)
def fund_wallet_checkout(wallet_id):
    amount = 1
    email = "khalfanathman12@gmail.com"
    phone = "254740403037"
    redirect_url = "http://example.com/thank-you"
    response = service.collect.checkout(wallet_id=wallet_id, phone_number=phone,
                                        email=email, amount=amount, currency="KES", 
                                        comment="Deposit", redirect_url=redirect_url)
    print(response.get("url"))
    return jsonify(response)

# INTERNAL TRANSFERS
@app_views.route('/wallets/<wallet_id>/transfer/<destination_id>',
                 methods=['POST'], strict_slashes=False)
def internal_wallet_transfer(wallet_id, destination_id):
    amount = 5000
    narrative = "Payment"
    origin_wallet_id =  wallet_id
    destination_wallet_id = destination_id
    response = service.wallets.intra_transfer(origin_wallet_id,
                                              destination_wallet_id,
                                              amount, narrative)
    print(response)

    return jsonify(response)

# EXTERNAL TRANSFER
@app_views.route('/wallets/<wallet_id>/transfer/',
                 methods=['POST'], strict_slashes=False)
def external_wallet_transfer(wallet_id):
    amount = 1
    email = "khalfanathman12@gmail.com"
    account1 = 254740403037
    account = 254719401851

    transactions = [{'name': 'Awesome Customer 1', 'account': account1, 'amount': 10},
                    {'name': 'Awesome Customer 2', 'account': account, 'amount': 10}]

    response = service.transfer.mpesa(wallet_id=wallet_id,
                                      currency='KES',
                                      transactions=transactions)
    print(response)
    approved_response = service.transfer.approve(response)
    print(approved_response)
    return jsonify(response)

#  TRANSACTION STATUS
@app_views.route('/transaction/<tracking_id>',
                 methods=['GET'], strict_slashes=False)
def get_transaction_status(tracking_id):
    status = service.transfer.status(tracking_id)
    str = f"Status: {status}"

    return jsonify(str)
