#!/usr/bin/python3
"""Flask web App"""
from models.amenity import Amenity
from api.v1.views import app_views
from models.city import City
from flask import jsonify
from models.place import Place
from models.review import Review
from models import storage
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """ return the status of the API"""

    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_count():
    """retrieves the number of each objects by type"""
    dic = {}
    dic["amenities"] = storage.count(Amenity)
    dic["cities"] = storage.count(City)
    dic["places"] = storage.count(Place)
    dic["reviews"] = storage.count(Review)
    dic["states"] = storage.count(State)
    dic["users"] = storage.count(User)
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
