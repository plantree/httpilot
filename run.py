#!/usr/bin/env python3
"""
Simple runner script for HTTPilot development.
"""

from src.app import create_app
import os

if __name__ == "__main__":
    # Create Flask app with development configuration
    app = create_app('development')
    
    # Get host and port from environment or use defaults
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    print(f"🚁 Starting HTTPilot on http://{host}:{port}")
    print("Available endpoints:")
    print("  - /              : Home page with documentation")
    print("  - /health        : Health check")
    print("  - /api           : API information")
    print("  - /get           : GET request testing")
    print("  - /post          : POST request testing")
    print("  - /status/<code> : Status code testing")
    print("  - /headers       : Request headers inspection")
    print("  - /delay/<sec>   : Delayed responses")
    print()
    
    app.run(host=host, port=port, debug=debug)