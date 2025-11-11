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
                    "/cookies/set": "Set cookies from query parameters and redirect to cookie list",
                    "/cookies/set/<name>/<value>": "Set a specific cookie and redirect to cookie list",
                    "/cookies/delete": "Delete cookies specified in query parameters and redirect to cookie list",
                },
                "Response Inspection": {
                    "/json": "Return sample JSON data",
                    "/xml": "Return sample XML data",
                    "/html": "Return sample HTML data",
                    "/response-headers": "Set custom response headers via query parameters (GET, POST)",
                },
                "Response Formats & Encoding": {
                    "/robots.txt": "Return robots.txt file",
                    "/brotli": "Return Brotli-compressed response",
                    "/deflate": "Return Deflate-compressed response",
                    "/gzip": "Return GZip-compressed response",
                    "/encoding/utf8": "Return UTF-8 encoded content",
                },
                "Cache Testing": {
                    "/cache": "Test HTTP caching (returns 304 if If-Modified-Since or If-None-Match headers present)",
                    "/cache/<seconds>": "Set Cache-Control header for specified seconds",
                    "/etag/<etag>": "Test ETag handling with If-None-Match and If-Match headers",
                },
                "Dynamic Data": {
                    "/delay/<seconds>": "Return delayed response with timing information (max 60 seconds)",
                    "/base64/encoding/<value>": "Encode string to base64url format",
                    "/base64/decoding/<value>": "Decode base64url-encoded string",
                    "/bytes/<n>": "Generate n random bytes (max 1MB, supports seed parameter)",
                    "/uuid": "Generate a random UUID4",
                    "/stream/<n>": "Stream n JSON responses (max 100)",
                    "/stream-bytes/<n>": "Stream n random bytes (max 100KB, supports seed and chunk_size parameters)",
                    "/drip": "Drip data over a duration with optional delay (supports duration, numbytes, code, delay parameters)",
                    "/links/<n>/<offset>": "Generate HTML page with n links (1-200 links, for testing crawlers)",
                    "/range/<numbytes>": "Support HTTP range requests for partial content (max 100KB, supports chunk_size and duration)",
                },
                "Redirects": {
                    "/redirect/<n>": "302 redirect n times (supports absolute/relative query parameter)",
                    "/absolute-redirect/<n>": "302 absolute redirect n times",
                    "/relative-redirect/<n>": "302 relative redirect n times",
                    "/redirect-to": "Redirect to any URL with custom status code (supports GET, POST, PUT, DELETE, PATCH, TRACE)",
                },
                "Images": {
                    "/image": "Return image based on Accept header (supports PNG, JPEG, WebP, SVG)",
                    "/image/png": "Return a simple PNG image",
                    "/image/jpeg": "Return a simple JPEG image",
                    "/image/webp": "Return a simple WebP image",
                    "/image/svg": "Return a simple SVG image",
                },
                "System": {
                    "/health": "Health check endpoint",
                    "/api": "API information and endpoint list",
                },
            },
        }
    )
