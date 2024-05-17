#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
import requests
import json

import requests
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
# Your Mpesa API keys

# Make a GET request to fetch the access token

@app_views.route('/access_token', methods=['GET'], strict_slashes=False)
def get_token():
    consumer_key = "ab6QiTm9tmKrcnIInmCJ9wiNcT7sw8n9csLbfcejdjXiNdk1"
    consumer_secret = "3YGaqYEOJ84rAGC1AsGWIDYdgwBd4seyAG4UH8A5LUNjrxf0fb46hc0QPLZRuHcQ"

# Access token URL
    access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
    status = response.status_code 
    if status == 200:
        access_token = response.json()['access_token']
        print(access_token)
        # print(f"Failed to get access token: {response.status_code}")
    return response.json()


@app_views.route('/register', methods=['GET'], strict_slashes=False)
def register():
    obj = get_token()
    access_token = obj['access_token']
    url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    json_data = {
        'ShortCode': '600996',
        'ResponseType': 'Complete',
        'ConfirmationURL': 'http://127.0.0.1:5001/confirmation',
        'ValidationURL': 'http://127.0.0.1:5001/validation_url'
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        return f"Error: {response.status_code}", 400

