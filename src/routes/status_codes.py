"""Status code testing routes."""

from flask import Blueprint, jsonify, abort
from werkzeug.exceptions import HTTPException

bp = Blueprint("status_codes", __name__)


@bp.route("/status/<int:code>", methods=["GET", "PUT", "PATCH", "POST", "OPTIONS"])
def status_code(code):
    """Return a response with the specified status code."""

    # Common status codes with descriptions
    status_descriptions = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        418: "I'm a teapot",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
    }

    description = status_descriptions.get(code, "Unknown Status Code")

    response_data = {
        "status": code,
        "message": description,
        "description": f"This is a {code} {description} response from HTTPilot",
    }

    # For 204 No Content, return empty response
    if code == 204:
        return "", 204

    # For redirect status codes, add location header
    if 300 <= code < 400:
        response = jsonify(response_data)
        response.status_code = code
        response.headers["Location"] = "/get"
        return response

    # For other status codes
    if code in status_descriptions:
        return jsonify(response_data), code
    else:
        # Handle unknown status codes
        abort(400)


@bp.route("/status/random", methods=["GET", "PUT", "PATCH", "POST", "OPTIONS"])
def random_status():
    """Return a random status code."""
    import random

    common_codes = [200, 201, 400, 401, 403, 404, 500, 502, 503]
    code = random.choice(common_codes)

    return status_code(code)
