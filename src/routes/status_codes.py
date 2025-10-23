"""Status code testing routes."""

from flask import Blueprint, jsonify, abort, make_response
from werkzeug.exceptions import HTTPException
import json

from .utils import utcnow

bp = Blueprint("status_codes", __name__)

REDIRECT_LOCATION = "/redirect/1"
ACCEPTED_MEDIA_TYPES = [
    "image/webp",
    "image/svg+xml",
    "image/jpeg",
    "image/png",
    "image/*",
]
ASCII_ART = """
    -=[ teapot ]=-

       _...._
     .'  _ _ `.
    | ."` ^ `". _,
    \_;`"---"`|//
      |       ;/
      \_     _/
        `\"\"\"`
"""


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

    redirect = dict(headers=dict(location=REDIRECT_LOCATION))

    code_map = {
        301: redirect,
        302: redirect,
        303: redirect,
        304: dict(data=""),
        305: redirect,
        306: redirect,
        307: redirect,
        401: dict(headers={"WWW-Authenticate": 'Basic realm="Fake Realm"'}),
        402: dict(
            data="Are you kidding?",
            headers={"x-more-info": "http://vimeo.com/22053820"},
        ),
        406: dict(
            data=json.dumps(
                {
                    "message": "Client did not request a supported media types.",
                    "accept": ACCEPTED_MEDIA_TYPES,
                }
            )
        ),
        407: dict(headers={"Proxy-Authenticate": 'Basic realm="Fake Realm"'}),
        418: dict(
            data=ASCII_ART,
            headers={"x-more-info": "http://tools.ietf.org/html/rfc2324"},
        ),
    }

    response = make_response()
    response.status_code = code

    # For 204 No Content, return empty response
    if code == 204:
        return response

    if code in code_map:
        value = code_map[code]
        if "data" in value:
            response.data = value["data"]
        if "headers" in value:
            response.headers = value["headers"]

    return response


@bp.route("/status/random", methods=["GET"])
def random_status():
    """Return a random status code."""
    import random

    common_codes = [200, 201, 400, 401, 403, 404, 500, 502, 503]
    code = random.choice(common_codes)

    return status_code(code)
