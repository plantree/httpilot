"""
Some shared functions.
"""
from datetime import datetime, timezone


def utcnow():
    """Return UTC timestamp of the current."""
    return datetime.now(timezone.utc).isoformat() + "Z"
