# utils.py
from functools import wraps
from flask import redirect, url_for, session, request
from flask_jwt_extended import decode_token
from datetime import datetime
import requests

def refresh_token():
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        return False
    url = "http://127.0.0.1:5001/auth/refresh"
    headers = {"Authorization": f"Bearer {refresh_token}"}
    res = requests.post(url=url, headers=headers)
    if res.status_code == 200:
        new_tokens = res.json()
        session["access_token"] = new_tokens["access_token"]
        session["refresh_token"] = new_tokens["refresh_token"]
        return True
    return False

def is_logged_in():
    try:
        # Check if the token is present in the session
        access_token = session.get("access_token")
        if not access_token:
            return False

        # Manually decode the JWT token
        decoded_token = decode_token(access_token)

        # Check the token expiry
        if decoded_token["exp"] < datetime.timestamp(datetime.now()):
            # Attempt to refresh the token if it has expired
            if not refresh_token():
                return False

        # Optionally, make a request to the `/who_am_i` endpoint to validate the token server-side
        url = "http://127.0.0.1:5001/auth/who_am_i"
        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Authentication error: {e}")  # Log the error for debugging
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("app_routes.login"))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    access_token = session.get("access_token")
    if not access_token:
        return None  # or handle as appropriate

    url = "http://127.0.0.1:5001/auth/who_am_i"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # This will contain the user's information
    else:
        return None  # or handle as appropriate
