# utils.py
from functools import wraps
from flask import redirect, url_for, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import jwt
from flask import session
from flask_jwt_extended import decode_token, get_jwt_identity
from datetime import datetime
import requests


def refresh_token():
    refresh_token = session.get('refresh_token')
    if not refresh_token:
        return False
    url = "http://127.0.0.1:5001/auth/refresh"
    headers = {'Authorization': f'Bearer {refresh_token}'}
    res = requests.post(url=url, headers=headers)
    if res.status_code == 200:
        new_tokens = res.json()
        session['access_token_cookie'] = new_tokens['access_token']
        session['csrf_access_token'] = new_tokens['csrf_access_token']
        return True
    return False

def is_logged_in():
    try:
        # Check if the tokens are present in the session
        access_token_cookie = session.get('access_token_cookie')
        csrf_access_token = session.get('csrf_access_token')
        if not access_token_cookie or not csrf_access_token:
            return False

        # Manually decode the JWT token
        decoded_token = decode_token(access_token_cookie)

        # Check the token expiry
        if decoded_token['exp'] < datetime.timestamp(datetime.now()):
            # Attempt to refresh the token if it has expired
            if not refresh_token():
                return False

        # Optionally, make a request to the `/who_am_i` endpoint to validate the token server-side
        url = "http://127.0.0.1:5001/auth/who_am_i"
        headers = {'Authorization': f'Bearer {access_token_cookie}'}
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            timestamp = res.headers.get('Current-Tk-Time')
            if timestamp is not None:
                timestamp2 = float(timestamp)
                dt_object = datetime.fromtimestamp(timestamp2)
                return True
            else:
                print("Authentication error: 'Current-Tk-Time' header is missing or None")
                return False
        else:
            return False
    except Exception as e:
        print(f"Authentication error: {e}")  # Log the error for debugging
        return False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('app_routes.login'))
        return f(*args, **kwargs)
    return decorated_function
