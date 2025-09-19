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


@bp.route("/response-headers", methods=["GET", "POST"])
def response_headers():
    """Returns a set of response headers from the query string."""
    # Common headers that should be treated specially
    headers = {}
    
    # Process query parameters as headers
    for key, value in request.args.items():
        headers[key.capitalize()] = value
    
    # Response data showing what headers were set
    response_data = {
        "message": "Custom response headers set",
        "headers_set": headers,
        "usage": "Add query parameters to set response headers. Example: /response-headers?X-Custom=value&Server=HTTPilot",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # Create response
    response = make_response(jsonify(response_data))
    
    # Set all custom headers
    for header_name, header_value in headers.items():
        response.headers.add(header_name, header_value)

    return response
