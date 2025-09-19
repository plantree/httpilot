# HTTPilot

🚁 A copilot tool to help understand HTTP requests and responses. Inspired by [httpbin](https://github.com/postmanlabs/httpbin).

HTTPilot is a Flask-based HTTP testing service that helps developers understand HTTP by providing various endpoints to test different HTTP methods, status codes, and request/response scenarios.

## Features

- **HTTP Methods Testing**: Test GET, POST, PUT, DELETE, PATCH, HEAD, and OPTIONS requests
- **Status Code Testing**: Return responses with specific HTTP status codes (supports multiple methods)
- **Request Inspection**: Analyze request headers, IP addresses, user agents, and cookies
- **Cookie Management**: Add random test cookies and clear existing cookies
- **Response Inspection**: Generate JSON, XML, HTML responses and customize response headers
- **Utilities**: Delayed responses for testing timeout scenarios
- **Web Interface**: Clean HTML interface with collapsible sections for easy endpoint exploration

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
- `GET /cookies` - Return cookies sent by client

### Cookie Management
- `GET /cookies/add` - Add random test cookies to response
- `GET /cookies/clear` - Clear all cookies from client

### Response Inspection
- `GET /json` - Return sample JSON data
- `GET /xml` - Return sample XML data
- `GET /html` - Return sample HTML data
- `GET|POST /response-headers` - Set custom response headers via query parameters

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
│   │   └── utils.py         # Utility routes
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