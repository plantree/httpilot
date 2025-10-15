"""Dynamic data routes."""

from flask import Blueprint, request, jsonify, make_response, Response
import base64
import time
import random

from .utils import utcnow

bp = Blueprint("dynamic_data", __name__)


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
            "timestamp": utcnow(),
            "message": f"Delayed response after {seconds} seconds",
        }
    )


@bp.route("/base64/decoding/<value>")
def base64_decoding(value):
    """Encodes the given string to base64url-encoded."""
    encoded = value.encode("utf-8")  # base64 expects a binary string
    try:
        return base64.urlsafe_b64decode(encoded).decode("utf-8")
    except:
        return "Incorrect Base64 data try: aGVsbG93b3JsZA==", 400


@bp.route("/base64/encoding/<value>")
def base64_encoding(value):
    """Decodes base64url-encoded string."""
    encoded = value.encode("utf-8")
    return base64.urlsafe_b64encode(encoded).decode("utf-8")


@bp.route("/bytes/<int:n>")
def random_bytes(n):
    """Returns n random bytes generated with given seed."""
    n = min(n, 1000 * 1024)  # 100kb limited
    if "seed" in request.args.items():
        random.seed(int(request.args["seed"]))

    response = make_response()

    response.data = bytearray(random.randint(0, 255) for i in range(n))
    response.content_type = "application/octet-stream"
    return response
