#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse.models import storage
from welpurse.models.member import Welfare
from welpurse.models.wallet import Wallet
from flask import abort, jsonify, make_response, request, Response
from flasgger.utils import swag_from
from intasend import APIService
import intasend
from intasend.exceptions import IntaSendBadRequest
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import os
import logging
import json
import requests

# Set up basic logging
logging.basicConfig(level=logging.INFO)

token = os.getenv("TOKEN")
publishable_key = os.getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)
# Set a timeout globally if possible (this is hypothetical and depends on the IntaSend library's implementation)
intasend.http_client = requests.Session()
intasend.http_client.request = lambda *args, **kwargs: requests.request(
    *args, timeout=10, **kwargs
)


@app_views.route("/welfares", methods=["GET"], strict_slashes=False)
def get_welfares():
    """Get all Welfares with member counts"""
    from flask import jsonify

    obj = {}
    all_welfares = storage.all(Welfare)

    welfares = []
    total_groups = len(all_welfares)
    obj["total_groups"] = total_groups
    for welfare in all_welfares.values():
        member_count = len(welfare.members)
        welfare_dict = welfare.to_dict()
        welfare_dict["member_count"] = member_count
        welfare_dict["members"] = [
            member.to_dict() for member in welfare.members
        ]  # Convert members to dicts
        welfare_dict["events"] = [
            event.to_dict() for event in welfare.events
        ]  # Convert event to dicts
        welfare_dict["requests"] = [
            request.to_dict() for request in welfare.requests
        ]
        welfare_dict["wallet"] = (
            welfare.wallet.to_dict() if welfare.wallet else None
        )
        welfares.append(welfare_dict)

    obj["data"] = welfares

    res = jsonify(obj)
    return make_response(res, 200)


@app_views.route(
    "/welfares/<welfare_id>", methods=["GET"], strict_slashes=False
)
def get_welfare(welfare_id):
    """Get all Welfares with member counts"""
    from flask import jsonify

    obj = {}
    welfare = storage.get(Welfare, welfare_id)

    if welfare:
        member_count = len(welfare.members)
        welfare_dict = welfare.to_dict()
        welfare_dict["member_count"] = member_count
        welfare_dict["members"] = [
            member.to_dict() for member in welfare.members
        ]  # Convert members to dicts
        welfare_dict["events"] = [
            event.to_dict() for event in welfare.events
        ]  # Convert event to dicts
        welfare_dict["requests"] = [
            request.to_dict() for request in welfare.requests
        ]  # Convert event to dicts
        welfare_dict["wallet"] = (
            welfare.wallet.to_dict() if welfare.wallet else None
        )
        return make_response(jsonify(welfare_dict), 200)

    res = jsonify(obj)
    return make_response(res, 200)


def create_wallet(label, welfare_id):
    """
    Create a wallet with the specified label and welfare ID.
    """
    try:
        logging.info("Attempting to create wallet with label: %s", label)
        response = service.wallets.create(
            currency="KES", label=label, can_disburse=True
        )
        # if response.status_code != 200:
        #     logging.error("Failed to create wallet, status code: %d", response.status_code)
        #     return None, "Failed to create wallet"
    except IntaSendBadRequest as e:
        try:
            error_data = json.loads(e.args[0])
            logging.error("IntaSendBadRequest error: %s", error_data)
            # if 'errors' in error_data and error_data['errors'][0]['code'] == 'invalid_request_data':
            #     detail = error_data['errors'][0]['detail']
            return 400, f"Invalid request data:"
        except (json.JSONDecodeError, IndexError, KeyError) as parse_error:
            logging.exception(
                "Error parsing IntaSendBadRequest response: %s", parse_error
            )
            return 400, "An unexpected error occurred"
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)
        return 400, "An unexpected error occurred"
    response.pop("updated_at", None)
    response["welfare_id"] = welfare_id
    return 200, response


@app_views.route("/welfares", methods=["POST"], strict_slashes=False)
def create_welfare():
    """
    Creates a Welfare. Expects JSON input with the structure of the Welfare model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ["name", "description", "special_events"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Validate 'special_events' as boolean
    if not isinstance(data["special_events"], bool):
        abort(
            400,
            description="Invalid data type for special_events. Must be a boolean.",
        )

    # Serialize 'contribution_modes' to a JSON string if it exists and is a list
    if "contribution_modes" in data and isinstance(
        data["contribution_modes"], list
    ):
        data["contribution_modes"] = json.dumps(data["contribution_modes"])
    elif "contribution_modes" in data and not isinstance(
        data["contribution_modes"], list
    ):
        abort(
            400,
            description="Invalid data type for contribution_modes. Must be a list.",
        )

    # Serialize 'eligibility_requirements' to a JSON string if it exists and is a list
    if "eligibility_requirements" in data and isinstance(
        data["eligibility_requirements"], list
    ):
        data["eligibility_requirements"] = json.dumps(
            data["eligibility_requirements"]
        )
    elif "eligibility_requirements" in data and not isinstance(
        data["eligibility_requirements"], list
    ):
        abort(
            400,
            description="Invalid data type for eligibility_requirements. Must be a list.",
        )

    # Serialize 'role_descriptions' to a JSON string if it exists and is a dict
    if "role_descriptions" in data and isinstance(
        data["role_descriptions"], dict
    ):
        data["role_descriptions"] = json.dumps(data["role_descriptions"])
    elif "role_descriptions" in data and not isinstance(
        data["role_descriptions"], dict
    ):
        abort(
            400,
            description="Invalid data type for role_descriptions. Must be a dict.",
        )

    # Serialize 'notification_preferences' to a JSON string if it exists and is a list
    if "notification_preferences" in data and isinstance(
        data["notification_preferences"], list
    ):
        data["notification_preferences"] = json.dumps(
            data["notification_preferences"]
        )
    elif "notification_preferences" in data and not isinstance(
        data["notification_preferences"], list
    ):
        abort(
            400,
            description="Invalid data type for notification_preferences. Must be a list.",
        )

    # Create the Welfare instance
    instance = Welfare(**data)

    try:
        code, data = create_wallet(instance.name, instance.id)
    except Exception as e:
        abort(400, description=str(e))

    # Save the Welfare instance
    if code == 200:
        final_data = {}
        if isinstance(data, Response):
            json_data = (
                data.json()
            )  # Convert the Response object to a JSON dictionary
            final_data.update(json_data)
            instance.save()
            wallet = Wallet(**final_data)
            wallet.save()
        else:
            instance.save()
            final_data.update(data)
            wallet = Wallet(**final_data)
            wallet.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/welfares/<welfare_id>", methods=["PUT"], strict_slashes=False
)
@swag_from("documentation/welfare/update_welfare.yml", methods=["PUT"])
def update_welfare(welfare_id):
    """
    Updates a Welfare
    """
    welfare = storage.get(Welfare, welfare_id)
    if not welfare:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(welfare, key, value)
    storage.save()
    return make_response(jsonify(welfare.to_dict()), 200)


@app_views.route(
    "/welfares/<welfare_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/welfare/delete_welfare.yml", methods=["PUT"])
def delete_welfare(welfare_id):
    """
    Updates a State
    """
    welfare = storage.get(Welfare, welfare_id)
    if not welfare:
        abort(404)

    storage.delete(welfare)
    storage.save()
    return make_response(jsonify({}), 204)
