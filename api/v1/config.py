#!/usr/bin/env python3
from datetime import timedelta
class Config:
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_SECRET_KEY = "e94d628d5bc552207aa4c4b1f6e87cb1"  # Change this!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = 'e94d628d5bc552207aa4c4b1f6e87cb1'
    SWAGGER = {
        'title': 'WelPurse Restful API',
        'uiversion': 1
    }