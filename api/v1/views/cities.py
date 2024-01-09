#!/usr/bin/python3
"""a view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def city_of_state(state_id):
    """retrive all city with matching state_id"""
    cityArray = []
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    for city in state.cities:
        cityArray.append(city.to_dict())

    if not cityArray:
        abort(404)

    return jsonify(cityArray)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrive a city with matching city_id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a city with matching city_id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return {}


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a city with association to the
    state_id passed"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    if not ('name' in request.get_json()):
        abort(400, 'Missing name')

    data = request.get_json()

    data['state_id'] = state_id

    city = City(**data)

    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update city with matching city_id"""
    invalid_key = ['id', 'state_id', 'created_at' 'updated_at']
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if not (key in invalid_key):
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
