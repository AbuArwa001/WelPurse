import requests
import json

import requests
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from intasend import APIService

token = "ISSecretKey_test_609b3704-801f-4bf0-ab22-5ee656c13f43"
publishable_key = "ISPubKey_test_c35935db-78d3-4b6f-8ec3-221edb0abae1"
service = APIService(token=token, publishable_key=publishable_key, test=True)


# Retrieve Wallets
@app_views.route('/wallets', methods=['GET'], strict_slashes=False)
def get_wallets():
    response = service.wallets.retrieve()
    # print(response)
        # print(f"Failed to get access token: {response.status_code}")
    return jsonify(response)

@app_views.route('/wallets/<wallet_id>', methods=['GET'], strict_slashes=False)
def get_wallet_by_id(wallet_id):
    response = service.wallets.details(wallet_id)
    # print(response)
        # print(f"Failed to get access token: {response.status_code}")
    return jsonify(response)

# CREATE WALLETS
@app_views.route('/wallets/', methods=['POST'], strict_slashes=False)
def create_wallet():
    response = service.wallets.create(currency="KES", label="EDUFUND", can_disburse=True)
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
