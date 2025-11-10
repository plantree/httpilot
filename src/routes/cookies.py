"""Cookie manipulation routes."""

from flask import Blueprint, redirect, request, jsonify, make_response, url_for

from .utils import utcnow

bp = Blueprint("cookies", __name__)


@bp.route("/cookies", methods=["GET"])
def view_cookies():
    """Return cookie data."""
    cookies = dict(request.cookies.items())
    response_data = {"cookies": cookies, "timestamp": utcnow()}
    return make_response(jsonify(response_data))


def secure_cookie():
    """Return true if cookie should have secure attribute."""
    return request.is_secure


@bp.route("/cookies/set")
def set_cookies():
    """Sets cookie(s) as provided by the query string and redirects to cookie list."""
    response = make_response(redirect(url_for("cookies.view_cookies")))
    for key, value in request.args.items():
        response.set_cookie(key=key, value=value, secure=secure_cookie(), httponly=True)

    return response


@bp.route("/cookies/set/<name>/<value>")
def set_cookie(name, value):
    """Sets a cookie and redirects to cookie list."""
    response = make_response(redirect(url_for("cookies.view_cookies")))
    response.set_cookie(key=name, value=value, secure=secure_cookie(), httponly=True)

    return response


@bp.route("/cookies/delete")
def delete_cookies():
    """Deletes cookie(s) as provided by the query string and redirects to cookie list."""
    response = make_response(redirect(url_for("cookies.view_cookies")))
    for key in request.args.keys():
        response.delete_cookie(key=key)

    return response
