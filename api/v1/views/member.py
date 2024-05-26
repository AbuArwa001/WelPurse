#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Member
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
import jwt
import datetime
import hashlib


@app_views.route('/members', methods=['GET'], strict_slashes=False)
def get_members():
    """ Get all Members """
    all_members = {}
    all_members = storage.all("Member")
    members = []
    for member in all_members.values():
        members.append(member.to_dict())
    res = jsonify(members)
    return make_response(res, 200)

@app_views.route('/members', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_member.yml', methods=['POST'])
def post_member():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = Member(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/check_email', methods=['GET'], strict_slashes=False)
def check_email():
    """Check if an email is already registered."""
    email_to_check = request.args.get('email', None)
    if email_to_check is None:
        return make_response(jsonify({"error": "Missing email parameter"}), 400)

    # Query the database for a member with the provided email
    session = storage._DBStorage__session
    member = session.query(Member).filter_by(email=email_to_check).first()
    email_exists = member is not None
    return make_response(jsonify({"email_exists": email_exists}), 200)


# get dependents for a user

"""
MEMBER WITH RELATION TO OTHER TABLES
CRUD
"""
#  MEMBER DEPENDENTS
@app_views.route('/members/<member_id>/dependents/', methods=['GET'], strict_slashes=False)
def get_member_dependents(member_id):
    """ Get all Members """
    member = storage.get(Member, member_id)
    if not member:
        abort(404)
    dependents = member.dependents

    # Prepare the response data
    dependents_list = [dependent.to_dict() for dependent in dependents]

    return make_response(jsonify(dependents_list), 200)

# BENEFCIARIES
@app_views.route('/members/<member_id>/beneficiaries/', methods=['GET'], strict_slashes=False)
def get_member_beneficiaries(member_id):
    """ Get all Member's beneficiaries"""
    member = storage.get(Member, member_id)
    if not member:
        abort(404)
    beneficiaries = member.beneficiaries

    # Prepare the response data
    beneficiaries_list = [beneficiary.to_dict() for beneficiary in beneficiaries]

    return make_response(jsonify(beneficiaries_list), 200)
