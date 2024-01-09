#!/usr/bin/python3
"""a view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenity():
    """retrive all city with matching state_id"""
    amenityArray = []
    amenities = storage.all(Amenity)

    for obj in amenities.values():
        amenityArray.append(obj.to_dict())

    return jsonify(amenityArray)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """retrive an amenity with matching amenity_id"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an amenity with matching amenity_id"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return {}


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """create an amenity"""

    if not request.get_json():
        return jsonify("Not a JSON"), 400

    if not ('name' in request.get_json()):
        abort(400, 'Missing name')

    data = request.get_json()


    newAmenity = Amenity(**data)

    storage.new(newAmenity)
    storage.save()

    return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity with matching amenity_id"""
    invalid_key = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if not (key in invalid_key):
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict())
