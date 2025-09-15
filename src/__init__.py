"""
HTTPilot - HTTP Copilot Tool
A Flask-based tool to help understand HTTP requests and responses.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .app import create_app

__all__ = ["create_app"]
