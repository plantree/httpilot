"""Image generation routes."""
from flask import Blueprint, request, Response
import os

from .status_codes import status_code

bp = Blueprint("image", __name__)

# Find the correct template folder when runing from a different location
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")


def resource(filename):
    path = os.path.join(tmpl_dir, filename)
    if not os.path.exists(path):
        return None
    return open(path, "rb").read()


@bp.route("/image")
def image():
    """Returns a simple image of the type suggest by the Accept header."""
    headers = request.headers
    if "accept" not in headers:
        return image_png()  # default media type to png

    accept = headers["accept"].lower()

    if "image/webp" in accept:
        return image_webp()
    elif "image/svg+xml" in accept:
        return image_svg()
    elif "image/jpeg" in accept:
        return image_jpeg()
    elif "image/png" in accept or "image/*" in accept:
        return image_png()
    else:
        return status_code(406)


@bp.route("/image/png")
def image_png():
    """Returns a simple PNG image."""
    data = resource("images/pig.png")
    return Response(data, headers={"Content-Type": "image/png"})


@bp.route("/image/jpeg")
def image_jpeg():
    """Returns a simple JPEG image."""
    data = resource("images/jackal.jpg")
    return Response(data, headers={"Content-Type": "image/jpeg"})


@bp.route("/image/webp")
def image_webp():
    """Returns a simple WEBP image."""
    data = resource("images/wolf.webp")
    return Response(data, headers={"Content-Type": "image/webp"})


@bp.route("/image/svg")
def image_svg():
    """Returns a simple SVG image."""
    data = resource("images/logo.svg")
    return Response(data, headers={"Content-Type": "image/svg+xml"})
