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
    try:
        res = requests.post(url=url, headers=headers)
        if res.status_code == 200:
            new_tokens = res.json()
            session["access_token"] = new_tokens["access_token"]
            session["refresh_token"] = new_tokens["refresh_token"]
            return True
        return False
    except Exception as e:
        print(f"Error during token refresh: {e}")
        return False

def is_logged_in():
    access_token = session.get("access_token")
    if not access_token:
        return False

    try:
        decoded_token = decode_token(access_token)
    except Exception as e:
        print(f"Authentication error: {e}")
        if "Signature has expired" in str(e):
            if refresh_token():
                access_token = session.get("access_token")
            else:
                session.pop("access_token", None)
                session.pop("refresh_token", None)
                return False
        else:
            return False

    try:
        url = "http://127.0.0.1:5001/auth/who_am_i"
        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get(url=url, headers=headers)
        return res.status_code == 200
    except Exception as e:
        print(f"Error during token validation: {e}")
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
        return None

    url = "http://127.0.0.1:5001/auth/who_am_i"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching current user: {e}")
        return None
