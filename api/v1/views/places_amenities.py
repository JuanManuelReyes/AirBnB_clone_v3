#!/usr/bin/python3
"""
Places_amenities instance
"""


from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models import amenity
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_by_place(place_id):
        """Get the amenities by place"""

        amenity = storage.get(Place, place_id)

        if amenity is None:
            abort(404)

        amenities = []

        for amenity in storage.all("Amenity").values():
            amenities.append(amenity.to_dict())

        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
        """Delete an Amenity"""
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            abort(404)

        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
        """Creates an Amenity"""

        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        amenities = place.amenities
        amenities.append(amenity)

        if amenity in amenities:
            return jsonify(amenity.to_dict(), 200)
