"""
Cache routes.
"""
from flask import Blueprint, request, jsonify, make_response
from werkzeug.http import http_date
import uuid

from .utils import utcnow
from .status_codes import status_code

bp = Blueprint("cache", __name__)


@bp.route("/cache", methods=["GET"])
def cache():
    """Returns a 304 if an `If-Modified-Since` header or `If-None-Match` is present."""
    is_conditional = request.headers.get("If-Modified-Since") or request.headers.get(
        "If-None-Match"
    )

    if is_conditional is None:
        response_data = {"timestamp": utcnow(), "message": "Returns with no cache"}
        response = make_response(jsonify(response_data))
        response.headers["Last-Modified"] = http_date()
        response.headers["ETag"] = uuid.uuid4().hex
        return response
    else:
        return status_code(304)


@bp.route("/cache/<int:value>", methods=["GET"])
def cache_control(value):
    """Sets a Cache-control header for n seconds."""
    response_data = {
        "message": f"Cache will be valid for {value} seconds",
        "timestamp": utcnow(),
    }
    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = f"public, max-age={value}"
    return response


@bp.route("/etag/<etag>", methods=["GET"])
def etag(etag):
    """Assumes the resource has the given etag and reposonds to If-None-Match and If-Match headers appropriately."""
    if_none_match = request.headers.get("If-None-Match")
    if_match = request.headers.get("If-Match")

    if if_none_match:
        if etag in if_none_match or "*" in if_none_match:
            response = status_code(304)
            response.headers["ETag"] = etag
            return response
    elif if_match:
        if etag not in if_match and "*" not in if_match:
            return status_code(412)
    # return normal response
    response_data = {"message": "Doesn't match any etags", "timestamp": utcnow()}
    response = make_response(jsonify(response_data))
    response.headers["ETag"] = etag
    return response
