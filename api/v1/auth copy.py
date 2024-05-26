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
import hashlib
from flask_jwt_extended import current_user
from .extensions import jwt

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/login", methods=["POST"],  strict_slashes=False)
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    hash_pwd = hashlib.md5(password.encode()).hexdigest()
    session = storage._DBStorage__session
    member = session.query(Member).filter_by(email=email).first()
    if not member or  member.email != email or hash_pwd != member.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=member.id)
    response = jsonify({'login': True})
    set_access_cookies(response, access_token)
    return response

# @app.route("/logout", methods=["DELETE"])
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]
#     jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
#     return jsonify(msg="Access token revoked")

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(member):
    return member


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    session = storage._DBStorage__session
    print(identity)
    return session.query(Member).filter_by(id=identity).one_or_none()

# @auth_blueprint.route('/login', methods=['POST'], strict_slashes=False)
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     remember_me = request.json.get('remember_me', False)
#     expires = timedelta(days=7) if remember_me else timedelta(hours=1)
#     provided_password_hash = hashlib.md5(password.encode()).hexdigest()
#     session = storage._DBStorage__session
#     member = session.query(Member).filter_by(email=email).first()
#     # Replace this with your user authentication logic
#     if email != member.email or provided_password_hash != member.password:
#         return jsonify({"msg": "Bad username or password"}), 401

#     # Create the token using the user's username as the identity
#     access_token = create_access_token(identity=email, expires_delta=expires)
#     # response = jsonify({'login': True})
#     # set_access_cookies(response, access_token)
#     # return response
#     return jsonify(access_token=access_token)

@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify({'refresh': True})
    set_access_cookies(response, new_access_token)
    return response


@auth_blueprint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        response.headers["Current-Tk-Time"] = target_timestamp
        response.headers["Current-Rm-Time"] = target_timestamp - exp_timestamp
        exp_timestamp
        if target_timestamp > exp_timestamp:
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)
            set_access_cookies(response, new_access_token)
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        pass
    return response


# @auth_blueprint.route('/check-login', methods=['GET'])
# @jwt_required()
# def check_login():
#     # If the token is valid, get_jwt_identity() will return the identity of the JWT
#     current_user = get_jwt_identity()
#     if current_user:
#         return jsonify(logged_in=True, user=current_user), 200
#     else:
#         return jsonify(logged_in=False, msg="User not logged in"), 401
    
@auth_blueprint.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        full_name=current_user.name,
        email=current_user.email,
    )
