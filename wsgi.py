"""
WSGI entry point for HTTPilot application.
Used for production deployment with WSGI servers like Gunicorn.
"""

from src.app import create_app
import os

# Create Flask application
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()