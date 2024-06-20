#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify, make_response, abort
import json


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Status of API"""


#     return jsonify({"status": "OK"})
# class CustomBadRequest(Exception):
#     status_code = 400

#     def __init__(self, message):
#         super().__init__()
#         self.message = message
#     def __repr__(self) -> str:
#         return jsonify({"BAD": "BAD REQUEST"})


@app_views.errorhandler(400)
def handle_bad_request(error):
    message = str(error)
    response = jsonify({"error": message})
    response.status_code = 400
    return response


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """Status of API"""
    # Simulate a bad request
    raise abort(400)


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def number_objects():
    """Retrieves the number of each objects by type"""

    num_objs = {}
    # for i in range(len(classes)):
    #     num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
