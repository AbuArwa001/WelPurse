#!/usr/bin/env python3
from datetime import timedelta
from os import getenv
import redis

ACCESS_EXPIRES = timedelta(hours=1)


class Config:
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = getenv("SECRET_KEY")
    SWAGGER = {"title": "WelPurse Restful API", "uiversion": 1}
    # Configure your Redis instance
    jwt_redis_blocklist = redis.StrictRedis(
        host="localhost", port=6379, db=0, decode_responses=True
    )
