"""Main routes for HTTPilot."""

from flask import Blueprint, render_template, jsonify
from .. import __version__

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Home page with API documentation."""
    return render_template("index.html", version=__version__)


@bp.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "HTTPilot is running"})


@bp.route("/api")
def api_info():
    """API information endpoint."""
    return jsonify(
        {
            "name": "HTTPilot",
            "version": __version__,
            "description": "A copilot tool to help understand HTTP",
            "endpoints": {
                "HTTP Methods": {
                    "/get": "GET request testing",
                    "/post": "POST request testing",
                    "/put": "PUT request testing",
                    "/delete": "DELETE request testing",
                    "/patch": "PATCH request testing",
                    "/head": "HEAD request testing",
                    "/options": "OPTIONS request testing",
                },
                "Status Codes": {"/status/<code>": "Return specific HTTP status code"},
                "Request Inspection": {
                    "/headers": "Return request headers",
                    "/ip": "Return client IP address",
                    "/user-agent": "Return user agent",
                    "/cookies": "Return cookies",
                },
                "Utilities": {
                    "/delay/<seconds>": "Delayed response",
                    "/json": "Return JSON data",
                    "/xml": "Return XML data",
                    "/html": "Return HTML data",
                },
            },
        }
    )
