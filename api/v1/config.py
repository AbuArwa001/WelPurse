#!/usr/bin/env python3
from datetime import timedelta
from os import getenv
class Config:
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")  # Change this!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = getenv("SECRET_KEY")
    SWAGGER = {
        'title': 'WelPurse Restful API',
        'uiversion': 1
    }