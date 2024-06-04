#!/usr/bin/python3
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token,
                                unset_jwt_cookies,
                                set_access_cookies,
                                jwt_required,
                                get_jwt_identity,
                                get_jwt)
from welpurse.models import storage
from welpurse.models.member import Member
from welpurse.models.role import Role
import hashlib
from flask_jwt_extended import current_user
from .extensions import jwt
from .config import Config
from .config import ACCESS_EXPIRES

auth_blueprint = Blueprint('auth', __name__)



@auth_blueprint.route("/login", methods=["POST"], strict_slashes=False)
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    hash_pwd = hashlib.md5(password.encode()).hexdigest()
    session = storage._DBStorage__session
    member = session.query(Member).filter_by(email=email).first()
    if not member or hash_pwd != member.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=member.id)
    response = jsonify({'login': True})
    set_access_cookies(response, access_token)
    return response

@jwt.user_identity_loader
def user_identity_lookup(member):
    if isinstance(member, Member):
        return member.id
    return member  # Assume it's already an ID if not a Member instance

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    session = storage._DBStorage__session
    return session.query(Member).filter_by(id=identity).one_or_none()

@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify({'refresh': True})
    set_access_cookies(response, new_access_token)
    return response
# @auth_blueprint.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.timestamp(datetime.now())
#         target_timestamp = datetime.timestamp(datetime.now() + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#     except (RuntimeError, KeyError):
#         # No valid JWT in request
#         pass
#     return response
@auth_blueprint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        response.headers["Current-Tk-Time"] = target_timestamp
        response.headers["Current-Rm-Time"] = target_timestamp - exp_timestamp
        if target_timestamp > exp_timestamp:
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)
            set_access_cookies(response, new_access_token)
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        pass
    return response

@auth_blueprint.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    session = storage._DBStorage__session
    current_user = session.query(Member).filter_by(id=current_user_id).first()

    roles = [role.name for role in current_user.roles]

    return jsonify(
        id=current_user.id,
        full_name=current_user.name,
        email=current_user.email,
        roles=roles
    )

@auth_blueprint.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    Config.jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    response = jsonify(msg="Access token revoked")
    unset_jwt_cookies(response)  # Clear JWT cookies
    return response

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = Config.jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

