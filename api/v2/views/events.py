#!/usr/bin/python3
"""Queries the Mpeas API and returns the authorization
"""
from api.v1.views import app_views
from welpurse_v2.models import storage
from welpurse_v2.models.member import Member

# from welpurse_v2.models.event import Event
from welpurse_v2.models.event import Event
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from intasend.exceptions import IntaSendBadRequest
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)


@app_views.route("/events/", methods=["GET"], strict_slashes=False)
def get_events():
    """Get all EVENTS"""
    time = "%Y-%m-%dT%H:%M:%S.%f"
    all_events = {}
    all_events = storage.all(Event)
    events = []
    for event in all_events.values():
        event.end_date = event.end_date.strftime(time)
        event.start_date = event.start_date.strftime(time)
        events.append(event.to_dict())
    res = jsonify(events)
    return make_response(res, 200)


@app_views.route("/events/<event_id>", methods=["GET"], strict_slashes=False)
def get_event(event_id):
    """Get One Beneficiaries"""
    time = "%Y-%m-%dT%H:%M:%S.%f"
    event = storage.get(Event, event_id)
    # print(event.end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    if not event:
        abort(404)
    event = event.to_dict()
    event["end_date"] = event["end_date"].strftime(time)
    event["start_date"] = event["start_date"].strftime(time)
    # print(event)
    res = jsonify(event)
    return make_response(res, 200)


@app_views.route("/events", methods=["POST"], strict_slashes=False)
def create_event():
    """
    Creates a Event. Expects JSON input with the structure of the Event model.
    """

    # Check if the input is JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Extract data from the request
    data = request.get_json()

    # Required fields validation
    required_fields = ["welfare_id", "event_date", "title"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create the Event instance
    instance = Event(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/events/<event_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/event/update_event.yml", methods=["PUT"])
def update_event(event_id):
    """
    Updates a State
    """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at", "status", "welfare_id"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(event, key, value)
    storage.save()
    return make_response(jsonify(event.to_dict()), 200)


@app_views.route(
    "/events/<event_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/event/delete_event.yml", methods=["DELETE"])
def delete_event(event_id):
    """
    Updates a State
    """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    storage.delete(event)
    storage.save()
    return make_response(jsonify({}), 204)
