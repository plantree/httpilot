"""Dynamic data routes."""

from flask import Blueprint, request, jsonify, make_response
import time
from datetime import datetime

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


# TODO
