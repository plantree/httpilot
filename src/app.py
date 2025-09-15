"""
Main Flask application module for HTTPilot.
"""

import os
import json
import time
from datetime import datetime
from urllib.parse import urlencode
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.exceptions import HTTPException


def create_app(config_name='development'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    # Register blueprints
    from .routes import main, http_methods, status_codes, inspect
    app.register_blueprint(main.bp)
    app.register_blueprint(http_methods.bp)
    app.register_blueprint(status_codes.bp)
    app.register_blueprint(inspect.bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found on this server.',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred.',
            'status': 500
        }), 500
    
    return app


def main():
    """Entry point for console script."""
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)