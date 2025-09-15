"""Request inspection routes."""

from flask import Blueprint, request, jsonify
import time
from datetime import datetime

bp = Blueprint("inspect", __name__)


@bp.route("/headers")
def get_headers():
    """Return request headers."""
    return jsonify(
        {"headers": dict(request.headers), "method": request.method, "url": request.url}
    )


@bp.route("/ip")
def get_ip():
    """Return client IP address."""
    # Try to get real IP from proxy headers
    real_ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP")
        or request.environ.get("REMOTE_ADDR")
    )

    return jsonify(
        {
            "origin": real_ip,
            "headers": {
                "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
                "X-Real-IP": request.headers.get("X-Real-IP"),
                "Remote-Addr": request.environ.get("REMOTE_ADDR"),
            },
        }
    )


@bp.route("/user-agent")
def get_user_agent():
    """Return user agent information."""
    return jsonify(
        {
            "user-agent": request.headers.get("User-Agent", "Unknown"),
            "accept": request.headers.get("Accept", ""),
            "accept-language": request.headers.get("Accept-Language", ""),
            "accept-encoding": request.headers.get("Accept-Encoding", ""),
        }
    )


@bp.route("/cookies")
def get_cookies():
    """Return cookies."""
    return jsonify({"cookies": dict(request.cookies)})


@bp.route("/delay/<int:seconds>")
def delay_response(seconds):
    """Return a delayed response."""
    if seconds > 60:
        return jsonify({"error": "Maximum delay is 60 seconds"}), 400

    start_time = time.time()
    time.sleep(seconds)
    end_time = time.time()

    return jsonify(
        {
            "delay": seconds,
            "actual_delay": round(end_time - start_time, 3),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": f"Delayed response after {seconds} seconds",
        }
    )


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
