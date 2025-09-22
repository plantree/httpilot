# HTTPilot

🚁 A copilot tool to help understand HTTP requests and responses. Inspired by [httpbin](https://github.com/postmanlabs/httpbin).

HTTPilot is a Flask-based HTTP testing service that helps developers understand HTTP by providing various endpoints to test different HTTP methods, status codes, and request/response scenarios.

## Status

✅ **Fully Functional** - All features implemented and tested  
✅ **Import Issues Fixed** - All module imports working correctly  
✅ **Interactive Web Interface** - Complete with curl examples for each endpoint  
✅ **Version Management** - Automated versioning with setuptools_scm  

## Features

- **HTTP Methods Testing**: Test GET, POST, PUT, DELETE, PATCH, HEAD, and OPTIONS requests with detailed curl examples
- **Status Code Testing**: Return responses with specific HTTP status codes (supports multiple methods)
- **Request Inspection**: Analyze request headers, IP addresses, and user agents
- **Cookie Management**: View, add random test cookies, and clear existing cookies for testing
- **Response Inspection**: Generate JSON, XML, HTML responses and customize response headers via query parameters
- **Cache Testing**: Test HTTP caching mechanisms with conditional requests, ETags, and Cache-Control headers
- **Utilities**: Delayed responses for testing timeout scenarios
- **Interactive Web Interface**: Clean HTML interface with collapsible sections and ready-to-use curl examples
- **Version Management**: Automated version control using setuptools_scm and Git tags

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd httpilot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env file with your preferred settings
```

### Running the Application

```bash
make run
```

The application will be available at `http://localhost:5000`

## API Endpoints

### HTTP Methods Testing
- `GET /get` - Test GET requests and view request information
- `POST /post` - Test POST requests with form data or JSON
- `PUT /put` - Test PUT requests with data
- `DELETE /delete` - Test DELETE requests
- `PATCH /patch` - Test PATCH requests with partial data
- `HEAD /head` - Test HEAD requests (headers only)
- `OPTIONS /options` - Test OPTIONS requests

### Status Codes
- `GET|POST|PUT|PATCH|OPTIONS /status/<code>` - Return response with specific HTTP status code
- `GET /status/random` - Return response with random status code

### Request Inspection
- `GET /headers` - Return request headers information
- `GET /ip` - Return client IP address
- `GET /user-agent` - Return user agent and browser information

### Cookie Management
- `GET /cookies` - Return cookies sent by client
- `GET /cookies/add` - Add random test cookies to response
- `GET /cookies/clear` - Clear all cookies from client

### Response Inspection
- `GET /json` - Return sample JSON data
- `GET /xml` - Return sample XML data
- `GET /html` - Return sample HTML data
- `GET|POST /response-headers` - Set custom response headers via query parameters

### Cache Testing
- `GET /cache` - Test HTTP caching (returns 304 if If-Modified-Since or If-None-Match headers present)
- `GET /cache/<seconds>` - Set Cache-Control header for specified seconds
- `GET /etag/<etag>` - Test ETag handling with If-None-Match and If-Match headers

### Utilities
- `GET /delay/<seconds>` - Return delayed response (max 60 seconds)

### System
- `GET /health` - Health check endpoint
- `GET /api` - API information and endpoint list

## Examples

### Testing GET requests with parameters
```bash
curl "http://localhost:5000/get?param1=value1&param2=value2"
```

### Testing POST requests with JSON data
```bash
curl -X POST http://localhost:5000/post \
  -H "Content-Type: application/json" \
  -d '{"key": "value", "number": 42}'
```

### Testing status codes with different methods
```bash
curl http://localhost:5000/status/404
curl -X POST http://localhost:5000/status/418  # I'm a teapot!
curl http://localhost:5000/status/random
```

### Testing cookie management
```bash
# Add random cookies
curl -c cookies.txt http://localhost:5000/cookies/add

# View current cookies
curl -b cookies.txt http://localhost:5000/cookies

# Clear all cookies
curl -c cookies.txt http://localhost:5000/cookies/clear
```

### Testing custom response headers
```bash
# Set custom headers via query parameters
curl -i "http://localhost:5000/response-headers?X-Custom=test&Server=HTTPilot"

# Using POST method
curl -X POST -i "http://localhost:5000/response-headers?Cache-Control=no-cache"
```

### Testing HTTP caching
```bash
# Basic cache test (first request - returns data with cache headers)
curl -i http://localhost:5000/cache

# Conditional request with If-Modified-Since (returns 304 Not Modified)
curl -i -H "If-Modified-Since: Thu, 01 Jan 1970 00:00:00 GMT" http://localhost:5000/cache

# Conditional request with If-None-Match (returns 304 Not Modified)
curl -i -H "If-None-Match: some-etag" http://localhost:5000/cache

# Set Cache-Control header for 5 minutes
curl -i http://localhost:5000/cache/300

# Set Cache-Control header for 1 hour
curl -i http://localhost:5000/cache/3600

# Test ETag handling
curl -i http://localhost:5000/etag/test123

# Test ETag with If-None-Match (returns 304 if matches)
curl -i -H "If-None-Match: test123" http://localhost:5000/etag/test123

# Test ETag with wildcard If-None-Match (returns 304)
curl -i -H "If-None-Match: *" http://localhost:5000/etag/test123

# Test ETag with If-Match (returns 412 if doesn't match)
curl -i -H "If-Match: other-etag" http://localhost:5000/etag/test123
```

### Testing delayed responses
```bash
curl http://localhost:5000/delay/3
```

### Inspecting request headers
```bash
curl -H "Custom-Header: test-value" http://localhost:5000/headers
```

## Development

### Version Management

This project uses `setuptools_scm` for automatic version management:

```bash
# Check current version
make version

# Create a new release tag
make tag VERSION=1.2.3

# Development versions are automatically generated
```

See [Version Management Guide](docs/VERSION_MANAGEMENT.md) for detailed information.

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

### Project Structure
```
httpilot/
├── src/                     # Source code
│   ├── __init__.py
│   ├── app.py               # Flask application factory
│   ├── routes/              # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py          # Main routes
│   │   ├── http_methods.py  # HTTP method testing routes
│   │   ├── status_codes.py  # Status code routes
│   │   ├── request_inspect.py # Request inspection routes
│   │   ├── response_inspect.py # Response inspection routes
│   │   ├── cookies.py       # Cookie management routes
│   │   ├── utilities.py     # Utility routes (delay, etc.)
│   │   └── utils.py         # Shared utility functions
│   ├── static/              # Static files (CSS, JS, images)
│   └── templates/           # Jinja2 templates
│       └── index.html
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_basic.py        # Basic functionality tests
│   ├── test_http_methods.py # HTTP methods tests
│   ├── test_status_codes.py # Status codes tests
│   ├── test_request_inspect.py # Request inspection tests
│   ├── test_response_inspect.py # Response inspection tests
│   └── test_cookies.py      # Cookie management tests
├── config/                  # Configuration files
├── config.py               # Application configuration
├── wsgi.py                 # WSGI entry point
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── Procfile               # Heroku deployment
├── .env.example           # Environment variables example
└── README.md              # This file
```

## Deployment

### Heroku
1. Create a Heroku app
2. Set environment variables
3. Deploy using Git:
```bash
git push heroku main
```

### Docker
```bash
# Build image
docker build -t httpilot .

# Run container
docker run -p 5000:5000 httpilot
```

## Troubleshooting

### Import Errors
If you encounter import errors when running the application, ensure you're using the correct Python path:

```bash
# Run from the project root directory
cd httpilot
python -m src.app

# Or use the make command
make run
```

### Common Issues
1. **ModuleNotFoundError**: Make sure you're in the correct directory and have activated your virtual environment
2. **Port already in use**: Change the port in `config.py` or kill the process using the port
3. **Missing dependencies**: Run `pip install -r requirements.txt`

### Development Setup
For development, ensure all relative imports are working correctly. The project uses relative imports within the `src/routes/` package:
```python
# Correct import style in route files
from .utils import utcnow
```

## Configuration

Environment variables can be set in a `.env` file:

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
HOST=0.0.0.0
PORT=5000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Reference

1. [httpbin](https://github.com/postmanlabs/httpbin) - HTTP Request & Response Service
2. [Flask Documentation](https://flask.palletsprojects.com/)
3. [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)