#!/usr/bin/python3
"""a view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_of_place(place_id):
    """retrive all review with matching place_id"""
    reviewArray = []
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    for review in place.reviews:
        reviewArray.append(review.to_dict())

    if not reviewArray:
        abort(404)

    return jsonify(reviewArray)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrive a review with matching review_id"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review with matching review_id"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return {}


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create a review with association to the
    place_id passed"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        return jsonify("Not a JSON"), 400

    if not ('text' in request.get_json()):
        abort(400, 'Missing text')

    if not ('user_id' in request.get_json()):
        abort(400, 'Missing user_id')

    data = request.get_json()

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id

    review = Review(**data)

    storage.new(review)
    storage.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update review with matching review_id"""
    invalid_key = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if not (key in invalid_key):
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict())
