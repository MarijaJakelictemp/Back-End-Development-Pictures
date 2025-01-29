from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200



######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is None:
        abort(404, description="Picture not found")
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    picture = request.get_json()

    # Ensure the incoming JSON has necessary fields
    required_fields = {"id", "pic_url", "event_country", "event_state", "event_city", "event_date"}
    if not all(field in picture for field in required_fields):
        return jsonify({"Message": "Missing required fields"}), 400

    # Check if the picture ID already exists
    if any(p["id"] == picture["id"] for p in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the new picture to the data list
    data.append(picture)

    return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    updated_picture = request.get_json()

    # Find the picture in the list
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = updated_picture  # Replace with the new data
            return jsonify(updated_picture), 200

    return jsonify({"Message": f"Picture with id {id} not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID"""
    global data  # Ensure we modify the global data list

    for i, picture in enumerate(data):
        if picture["id"] == id:
            del data[i]  # Remove the picture
            return "", 204  # Success

    return jsonify({"Message": f"Picture with id {id} not found"}), 404
