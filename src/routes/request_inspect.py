"""Request inspection routes."""

from flask import Blueprint, request, jsonify

bp = Blueprint("request_inspect", __name__)


@bp.route("/headers")
def get_headers():
    """Return request headers."""
    return jsonify({"headers": dict(request.headers)})


@bp.route("/ip")
def get_ip():
    """Return client IP address."""
    # Try to get real IP from proxy headers
    real_ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP")
        or request.environ.get("REMOTE_ADDR")
    )

    return jsonify({"origin": real_ip})


@bp.route("/user-agent")
def get_user_agent():
    """Return user agent information."""
    return jsonify(
        {
            "user-agent": request.headers.get("User-Agent", "Unknown"),
        }
    )
