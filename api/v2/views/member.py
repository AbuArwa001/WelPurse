#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse_v2.models import storage
from welpurse_v2.models.member import Member
from welpurse_v2.models.welfare import Welfare
from welpurse_v2.models.associations import welfaremembers
from welpurse_v2.models.role import Role
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
import jwt
import datetime
import hashlib


@app_views.route("/members", methods=["GET"], strict_slashes=False)
def get_members():
    """Get all Members"""
    all_members = {}
    all_members = storage.all("Member")
    members = []
    for member in all_members.values():
        members.append(member.to_dict())
    res = jsonify(members)
    return make_response(res, 200)


@app_views.route("/members/<member_id>", methods=["GET"], strict_slashes=False)
def get_member(member_id):
    """Get all Members"""
    member = storage.get(Member, member_id)
    if not member:
        abort(404)
    res = jsonify(member.to_dict())
    return make_response(res, 200)


@app_views.route("/members", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user/post_member.yml", methods=["POST"])
def post_member():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "email" not in request.get_json():
        abort(400, description="Missing email")
    if "password" not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = Member(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/check_email", methods=["GET"], strict_slashes=False)
def check_email():
    """Check if an email is already registered."""
    email_to_check = request.args.get("email", None)
    if email_to_check is None:
        return make_response(
            jsonify({"error": "Missing email parameter"}), 400
        )

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
@app_views.route(
    "/members/<member_id>/dependents/", methods=["GET"], strict_slashes=False
)
def get_member_dependents(member_id):
    """Get all Members"""
    member = storage.get(Member, member_id)
    if not member:
        abort(404)
    dependents = member.dependents

    # Prepare the response data
    dependents_list = [dependent.to_dict() for dependent in dependents]

    return make_response(jsonify(dependents_list), 200)


# BENEFCIARIES
@app_views.route(
    "/members/<member_id>/beneficiaries/",
    methods=["GET"],
    strict_slashes=False,
)
def get_member_beneficiaries(member_id):
    """Get all Member's beneficiaries"""
    member = storage.get(Member, member_id)
    if not member:
        abort(404)
    beneficiaries = member.beneficiaries

    # Prepare the response data
    beneficiaries_list = [
        beneficiary.to_dict() for beneficiary in beneficiaries
    ]

    return make_response(jsonify(beneficiaries_list), 200)


"""
ADJUST ROLES TO MEMBER
"""


@app_views.route(
    "/members/<member_id>/roles/<role_id>",
    methods=["POST"],
    strict_slashes=False,
)
def add_role_to_member(member_id, role_id):
    member = storage.get(Member, member_id)
    role = storage.get(Role, role_id)
    if member is None or role is None:
        abort(404)
    if role not in member.roles:
        member.roles.append(role)
        storage.save()

    # Convert member to dictionary and include roles
    member_dict = member.to_dict()
    member_dict["roles"] = [role.to_dict() for role in member.roles]

    return jsonify(member_dict), 200


@app_views.route(
    "/members/<member_id>/roles/<role_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def remove_role_from_member(member_id, role_id):
    member = storage.get(Member, member_id)
    role = storage.get(Role, role_id)
    if member is None or role is None:
        abort(404)

    if role in member.roles:
        member.roles.remove(role)
        storage.save()

    member_dict = member.to_dict()
    member_dict["roles"] = [role.to_dict() for role in member.roles]
    return jsonify(member_dict), 200


@app_views.route(
    "/members/<member_id>/roles/", methods=["PUT"], strict_slashes=False
)
def edit_member_roles(member_id):
    data = request.get_json()
    if data is None or "roles" not in data:
        abort(400, "Roles data not provided")

    member = storage.get(Member, member_id)
    if member is None:
        abort(404)

    new_roles_ids = data["roles"]
    new_roles = [storage.get(Role, role_id) for role_id in new_roles_ids]
    if None in new_roles:
        abort(404, "One or more roles not found")

    # Convert Role objects to dictionaries before assigning to member.roles
    member.roles = [role for role in new_roles if hasattr(role, "to_dict")]
    storage.save()

    # Convert the member object to a dictionary and include the roles
    member_dict = member.to_dict()
    member_dict["roles"] = [role.to_dict() for role in member.roles]

    return jsonify(member_dict), 200


@app_views.route(
    "/members/<member_id>/roles/", methods=["GET"], strict_slashes=False
)
def get_member_roles(member_id):
    member = storage.get(Member, member_id)
    if member is None:
        abort(404)

    roles = [
        role.to_dict() for role in member.roles if hasattr(role, "to_dict")
    ]

    return jsonify(roles), 200


"""
MAKE MEMBER JOIN THE GROUP
"""


@app_views.route("/join_group", methods=["POST"], strict_slashes=False)
def join_group():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    # Fetch the member and welfare instances
    member = storage.get(Member, data["member_id"])
    welfare = storage.get(Welfare, data["welfare_id"])

    if not member or not welfare:
        return jsonify({"error": "Member or Welfare not found"}), 404

    # Che ck if the member is already part of the welfare
    if member in welfare.members:
        return jsonify({"error": "Member already part of the Welfare"}), 400

    # Create a new WelfareMember association
    new_welfare_member = welfare.members.append(member)
    storage.save()
    return jsonify({"message": "Member successfully added to Welfare"}), 200


"""
GET MEMBERS FROM WELFARE
"""


@app_views.route(
    "/welfares/<welfare_id>/members", methods=["GET"], strict_slashes=False
)
def get_members_for_welfare(welfare_id):
    welfare = storage.get(Welfare, welfare_id)
    if not welfare:
        abort(404, description="WELFARE NOT FOUND")
    members = []
    for member in welfare.members:
        members.append(member.to_dict())
    res = jsonify(members)
    return make_response(res, 200)


@app_views.route(
    "/welfares/<welfare_id>/members/<member_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def remove_member_for_welfare(welfare_id, member_id):

    welfare = storage.get(Welfare, welfare_id)
    if not welfare:
        abort(404, description="WELFARE NOT FOUND")
    member = storage.get(Member, member_id)
    members = welfare.members
    if member in members:
        members.remove(member)
    return make_response({}, 200)
