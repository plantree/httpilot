"""Response inspection routes."""

from flask import Blueprint, request, jsonify, make_response
from datetime import datetime

bp = Blueprint("response_inspect", __name__)


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
            "timestamp": datetime.utcnow().isoformat() + "Z",
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
        datetime.utcnow().isoformat() + "Z"
    )

    response = jsonify(xml_data)
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
        datetime.utcnow().isoformat() + "Z"
    )

    response = jsonify(html_data)
    response.headers["Content-Type"] = "text/html"
    return response
