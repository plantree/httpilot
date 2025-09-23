"""Cookie manipulation routes."""

from flask import Blueprint, request, jsonify, make_response

from .utils import utcnow

bp = Blueprint("cookies", __name__)


@bp.route("/cookies", methods=["GET"])
def view_cookies():
    """Return cookie data."""
    cookies = dict(request.cookies.items())
    response_data = {"cookies": cookies, "timestamp": utcnow()}
    return make_response(jsonify(response_data))


@bp.route("/cookies/add", methods=["GET"])
def mock_cookies():
    """Add mock cookies with random values to the response."""
    import random
    import string

    # Generate random cookie values
    def generate_random_string(length=12):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    # Generate random cookie data
    token = generate_random_string(32)

    response_data = {
        "message": "Random cookies added successfully",
        "cookies_set": {"token": token},
        "timestamp": utcnow(),
    }

    response = make_response(jsonify(response_data))

    # Set random cookies with different max_age values
    response.set_cookie("token", token, max_age=1800)  # 30 minutes

    return response


@bp.route("/cookies/clear", methods=["GET"])
def clear_cookies():
    """Clear all cookies."""
    # Get all current cookies
    current_cookies = dict(request.cookies)

    response_data = {
        "message": "All cookies cleared successfully",
        "cookies_cleared": list(current_cookies.keys()) if current_cookies else [],
        "count": len(current_cookies),
        "timestamp": utcnow(),
    }

    response = make_response(jsonify(response_data))

    # Clear all existing cookies by setting them to expire
    for cookie_name in current_cookies:
        response.set_cookie(cookie_name, "", expires=0)

    return response


# TODO
