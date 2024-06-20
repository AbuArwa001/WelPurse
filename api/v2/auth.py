# auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    get_jwt_identity, 
    jwt_required, 
    get_jwt
)
from datetime import datetime, timezone, timedelta
import hashlib
import requests
from welpurse_v2.models import storage
from welpurse_v2.models.member import  Member
from .extensions import jwt
from .config import Config

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    hash_pwd = hashlib.md5(password.encode()).hexdigest()
    session = storage._DBStorage__session
    try:
        member = session.query(Member).filter_by(email=email).first()
        if not member or hash_pwd != member.password:
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=member.id)
        response = jsonify({"login": True})
        response.headers['Authorization'] = f'Bearer {access_token}'
        return response
    except Exception as e:
        session.rollback()
        print(f"Error during login query: {e}")
        return jsonify({"msg": "Internal server error"}), 500
    finally:
        session.close()

@jwt.user_identity_loader
def user_identity_lookup(member):
    return member.id if isinstance(member, Member) else member

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    session = storage._DBStorage__session
    return session.query(Member).filter_by(id=identity).one_or_none()

@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify({"refresh": True})
    response.headers['Authorization'] = f'Bearer {new_access_token}'
    return response

@auth_blueprint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        if target_timestamp > exp_timestamp:
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)
            response.headers['Authorization'] = f'Bearer {new_access_token}'
    except (RuntimeError, KeyError):
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
        roles=roles,
    )

@auth_blueprint.route('/logout', methods=["GET",'POST'], strict_slashes=False)
@jwt_required()
def logout():
    response = jsonify({"logout": True})
    response.headers['Authorization'] = ''
    return response

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = Config.jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
