"""
HTTPilot - HTTP Copilot Tool
A Flask-based tool to help understand HTTP requests and responses.
"""

try:
    from ._version import __version__
except ImportError:
    # fallback for development without proper Git setup
    __version__ = "unknown"

__author__ = "plantree"

from .app import create_app

__all__ = ["create_app", "__version__"]
