"""Response inspection routes."""

from flask import Blueprint, request, jsonify, make_response


bp = Blueprint("response_inspect", __name__)


@bp.route("/response-headers", methods=["GET", "POST"])
def response_headers():
    """Returns a set of response headers from the query string."""
    # Common headers that should be treated specially
    headers = {}

    # Process query parameters as headers
    for key, value in request.args.items():
        headers[key.capitalize()] = value

    response = make_response(jsonify(headers))

    for header_name, header_value in headers.items():
        response.headers.add(header_name, header_value)

    return response
