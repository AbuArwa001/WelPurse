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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JSONIFY_PRETTYPRINT_REGULAR = True
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SECRET_KEY = getenv("SECRET_KEY")
    SWAGGER = {"title": "WelPurse Restful API", "uiversion": 1}
    # Configure your Redis instance
    jwt_redis_blocklist = redis.StrictRedis(
        host="localhost", port=6379, db=0, decode_responses=True
    )
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_BINDS = {"default": SQLALCHEMY_DATABASE_URI}
    