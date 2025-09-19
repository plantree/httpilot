"""HTTP methods testing routes."""

from flask import Blueprint, request, jsonify

from .utils import utcnow

bp = Blueprint("http_methods", __name__)


def get_request_info():
    """Get common request information."""
    return {
        "method": request.method,
        "url": request.url,
        "args": dict(request.args),
        "headers": dict(request.headers),
        "origin": request.environ.get("REMOTE_ADDR"),
        "timestamp": utcnow(),
    }


@bp.route("/get", methods=["GET"])
def test_get():
    """Test GET requests."""
    info = get_request_info()
    return jsonify(info)


@bp.route("/post", methods=["POST"])
def test_post():
    """Test POST requests."""
    info = get_request_info()

    # Add form data
    if request.form:
        info["form"] = dict(request.form)

    # Add JSON data
    if request.is_json:
        try:
            info["json"] = request.get_json()
        except Exception as e:
            info["json_error"] = str(e)

    # Add raw data
    if request.data:
        try:
            info["data"] = request.data.decode("utf-8")
        except UnicodeDecodeError:
            info["data"] = f"<binary data, {len(request.data)} bytes>"

    return jsonify(info)


@bp.route("/put", methods=["PUT"])
def test_put():
    """Test PUT requests."""
    info = get_request_info()

    if request.is_json:
        try:
            info["json"] = request.get_json()
        except Exception as e:
            info["json_error"] = str(e)

    if request.data:
        try:
            info["data"] = request.data.decode("utf-8")
        except UnicodeDecodeError:
            info["data"] = f"<binary data, {len(request.data)} bytes>"

    return jsonify(info)


@bp.route("/delete", methods=["DELETE"])
def test_delete():
    """Test DELETE requests."""
    info = get_request_info()
    return jsonify(info)


@bp.route("/patch", methods=["PATCH"])
def test_patch():
    """Test PATCH requests."""
    info = get_request_info()

    if request.is_json:
        try:
            info["json"] = request.get_json()
        except Exception as e:
            info["json_error"] = str(e)

    return jsonify(info)


@bp.route("/head", methods=["HEAD"])
def test_head():
    """Test HEAD requests."""
    # HEAD requests should not return a body
    return "", 200


@bp.route("/options", methods=["OPTIONS"])
def test_options():
    """Test OPTIONS requests."""
    response = jsonify(get_request_info())
    response.headers["Allow"] = "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS"
    return response
