#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.welfare import Welfare
# from welpurse.models.role import Role
from welpurse.models.role import Role
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
import logging
# Set up basic logging
logging.basicConfig(level=logging.INFO)

@app_views.route('/roles', methods=['GET'], strict_slashes=False)
def get_roles():
    """ Get all Beneficiaries """
    all_roles = {}
    all_roles = storage.all(Role)
    roles = []
    for role in all_roles.values():
        roles.append(role.to_dict())
    res = jsonify(roles)
    return make_response(res, 200)

@app_views.route('/roles/<role_id>', methods=['GET'], strict_slashes=False)
def get_role(role_id):
    """ Get One Beneficiaries """
    role = storage.get(Role, role_id)
    if not role:
        abort(404)
    res = jsonify(role.to_dict())
    return make_response(res, 200)

@app_views.route('/roles', methods=['POST'], strict_slashes=False)
def create_role():
    """
    Creates a Role. Expects JSON input with the structure of the Role model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ['name']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the Role instance
    instance = Role(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/roles/<role_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/role/update_role.yml', methods=['PUT'])
def update_role(role_id):
    """
    Updates a State
    """
    role = storage.get(Role, role_id)
    if not role:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(role, key, value)
    storage.save()
    return make_response(jsonify(role.to_dict()), 200)

@app_views.route('/roles/<role_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/role/delete_role.yml', methods=['DELETE'])
def delete_role(role_id):
    """
    Updates a State
    """
    role = storage.get(Role, role_id)
    if not role:
        abort(404)

    storage.delete(role)
    storage.save()
    return make_response(jsonify({}), 204)
