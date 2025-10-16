"""Response format routes."""

from flask import Blueprint, render_template, jsonify, make_response

from .utils import utcnow
from . import filters


bp = Blueprint("request_format", __name__)

ROBOT_TXT = """User-agent: *
Disallow: /deny
"""


@bp.route("/json")
def return_json():
    """Return sample JSON data."""
    return jsonify(
        {
            "name": "HTTPilot",
            "version": "0.1.0",
            "description": "HTTP testing tool",
            "features": [
                "HTTP method testing",
                "Status code testing",
                "Request inspection",
                "Response formatting",
            ],
            "timestamp": utcnow(),
            "sample_data": {
                "number": 42,
                "boolean": True,
                "null_value": None,
                "array": [1, 2, 3, 4, 5],
            },
        }
    )


@bp.route("/xml")
def return_xml():
    """Return sample XML data."""
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<httpilot>
    <name>HTTPilot</name>
    <version>0.1.0</version>
    <description>HTTP testing tool</description>
    <features>
        <feature>HTTP method testing</feature>
        <feature>Status code testing</feature>
        <feature>Request inspection</feature>
        <feature>Response formatting</feature>
    </features>
    <timestamp>{}</timestamp>
</httpilot>""".format(
        utcnow()
    )

    response = make_response(xml_data)
    response.headers["Content-Type"] = "application/xml"
    return response


@bp.route("/html")
def return_html():
    """Return sample HTML data."""
    html_data = """<!DOCTYPE html>
<html>
<head>
    <title>HTTPilot</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>HTTPilot</h1>
    <p>A copilot tool to help understand HTTP</p>
    <ul>
        <li>HTTP method testing</li>
        <li>Status code testing</li>
        <li>Request inspection</li>
        <li>Response formatting</li>
    </ul>
    <p>Generated at: {}</p>
</body>
</html>""".format(
        utcnow()
    )

    response = make_response(html_data)
    response.headers["Content-Type"] = "text/html"
    return response


@bp.route("/robots.txt")
def robots():
    """Returns some robots.txt rules."""
    response = make_response(ROBOT_TXT)
    response.content_type = "text/plain"
    return response


@bp.route("/brotli")
@filters.brotli
def brotli():
    """Returns Brotli-encoded data."""
    response_data = {"timestamp": utcnow(), "message": "Get Brotli-encoded data"}
    return jsonify(response_data)


@bp.route("/deflate")
@filters.deflate
def deflate():
    """Returns Deflate-encoded data."""
    response_data = {"timestamp": utcnow(), "message": "Get Deflate-encoded data"}
    return jsonify(response_data)


@bp.route("/gzip")
@filters.gzip
def gzip():
    """Returns GZip-encoded data."""
    response_data = {"timestamp": utcnow(), "message": "Get GZip-encoded data"}
    return jsonify(response_data)


@bp.route("/encoding/utf8")
def encoding_utf8():
    """Returns a UTF-8 encoded body."""
    return render_template("utf8-demo.txt")
