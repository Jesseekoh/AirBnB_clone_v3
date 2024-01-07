#!/usr/bin/python3
"""Flask web App"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """ return the status of the API"""

    return jsonify({"status": "OK"})
