#!/usr/bin/python3
"""a view for User objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_user():
    """retrive all user object"""
    userArray = []
    users = storage.all(User)

    for obj in users.values():
        userArray.append(obj.to_dict())

    return jsonify(userArray)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """retrive a user with matching user_id"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a user with matching user_id"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return {}


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """create a User Object"""

    if not request.get_json():
        return jsonify("Not a JSON"), 400

    if not ('email' in request.get_json()):
        abort(400, 'Missing email')

    if not ('password' in request.get_json()):
        abort(400, 'Missing password')

    data = request.get_json()

    newUser = User(**data)

    storage.new(newUser)
    storage.save()

    return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update user with matching user_id"""
    invalid_key = ['id', 'created_at', 'email', 'updated_at']
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if not (key in invalid_key):
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict())
