#!/usr/bin/python3
"""Flask app"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from os import getenv
from models import storage

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def cleanUp(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    error_dic = {"error": "Not found"}
    return jsonify(error_dic), 404


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
