#!/usr/bin/python3
"""a view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_of_city(city_id):
    """retrive all place with matching city_id"""
    placeArray = []
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    for place in city.places:
        placeArray.append(place.to_dict())

    if not placeArray:
        abort(404)

    return jsonify(placeArray)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrive a place with matching place_id"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place with matching place_id"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return {}


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place with association to the
    city_id passed"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        return jsonify("Not a JSON"), 400

    if not ('name' in request.get_json()):
        abort(400, 'Missing name')

    if not ('user_id' in request.get_json()):
        abort(400, 'Missing user_id')

    data = request.get_json()

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id

    place = Place(**data)

    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update place with matching place_id"""
    invalid_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if not (key in invalid_key):
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())
