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
                "Status Codes": {
                    "/status/<code>": "Return specific HTTP status code (supports GET, POST, PUT, PATCH, OPTIONS)",
                    "/status/random": "Return random HTTP status code (GET only)",
                },
                "Request Inspection": {
                    "/headers": "Return request headers",
                    "/ip": "Return client IP address",
                    "/user-agent": "Return user agent information",
                },
                "Cookie Management": {
                    "/cookies": "Return cookies sent by client",
                    "/cookies/add": "Add random test cookies to response",
                    "/cookies/clear": "Clear all cookies from client",
                },
                "Response Inspection": {
                    "/json": "Return sample JSON data",
                    "/xml": "Return sample XML data",
                    "/html": "Return sample HTML data",
                    "/response-headers": "Set custom response headers via query parameters (GET, POST)",
                },
                "Cache Testing": {
                    "/cache": "Test HTTP caching (returns 304 if If-Modified-Since or If-None-Match headers present)",
                    "/cache/<seconds>": "Set Cache-Control header for specified seconds",
                    "/etag/<etag>": "Test ETag handling with If-None-Match and If-Match headers",
                },
                "Utilities": {
                    "/delay/<seconds>": "Return delayed response (max 60 seconds)",
                },
                "System": {
                    "/health": "Health check endpoint",
                    "/api": "API information and endpoint list",
                },
            },
        }
    )
