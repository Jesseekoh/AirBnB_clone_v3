#!/usr/bin/python3
"""View for State objects that handles default API actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_states(id=None):
    """retrive all states or based on
    id passed"""
    states = storage.all("State")
    if not id:
        all_state = []

        for obj in states.values():
            all_state.append(obj.to_dict())

        return jsonify(all_state)

    for obj in states.values():
        if obj.id == id:
            return jsonify(obj.to_dict())

    abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Delete state with matching id"""
    states = storage.all()

    if not state_id:
        abort(404)

    for obj in states.values():
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
            return {}

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create New state"""
    if not request.get_json():
        return jsonify("Not a JSON"), 400

    if not ('name' in request.get_json()):
        return jsonify("Missing name"), 400

    data = request.get_json()

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update state with matching id"""
    invalid_keys = ['updated_at', 'id', 'created_at']

    if not request.get_json():
        return jsonify("Not a JSON"), 400

    json_data = request.get_json()

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    or key, value in json_data.items():
        if not (key in invalid_keys):
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict())
