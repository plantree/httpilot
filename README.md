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
- **Response Formats & Encoding**: Test various response formats and compression algorithms (Brotli, GZip, Deflate, UTF-8)
- **Cache Testing**: Test HTTP caching mechanisms with conditional requests, ETags, and Cache-Control headers
- **Dynamic Data**: Time-sensitive responses, base64 encoding/decoding, random data generation, UUID generation, streaming data, data dripping, link generation, and HTTP range requests
- **Redirects**: Test HTTP redirect behavior with configurable redirect counts and absolute/relative URL options
- **Images**: Content negotiation for different image formats (PNG, JPEG, WebP, SVG) with proper HTTP headers
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
- `GET|POST /cookies/set` - Set cookies from query parameters (redirects to /cookies)
- `GET|POST /cookies/set/<name>/<value>` - Set specific cookie and redirect
- `GET|POST /cookies/delete` - Delete cookies specified in query parameters

### Response Inspection
- `GET /json` - Return sample JSON data
- `GET /xml` - Return sample XML data
- `GET /html` - Return sample HTML data
- `GET|POST /response-headers` - Set custom response headers via query parameters

### Response Formats & Encoding
- `GET /robots.txt` - Return robots.txt file with crawling rules
- `GET /brotli` - Return Brotli-compressed response data
- `GET /deflate` - Return Deflate-compressed response data
- `GET /gzip` - Return GZip-compressed response data
- `GET /encoding/utf8` - Return UTF-8 encoded content with international characters

### Cache Testing
- `GET /cache` - Test HTTP caching (returns 304 if If-Modified-Since or If-None-Match headers present)
- `GET /cache/<seconds>` - Set Cache-Control header for specified seconds
- `GET /etag/<etag>` - Test ETag handling with If-None-Match and If-Match headers

### Dynamic Data
- `GET /delay/<seconds>` - Return delayed response with timing information (max 60 seconds)
- `GET /base64/encoding/<value>` - Encode string to base64url format
- `GET /base64/decoding/<value>` - Decode base64url-encoded string
- `GET /bytes/<n>` - Generate n random bytes (max 1MB, supports seed parameter)
- `GET /uuid` - Generate a random UUID4
- `GET /stream/<n>` - Stream n JSON responses (max 100)
- `GET /stream-bytes/<n>` - Stream n random bytes (max 100KB, supports seed and chunk_size parameters)
- `GET /drip` - Drip data over a duration with optional delay (supports duration, numbytes, code, delay parameters)
- `GET /links/<n>/<offset>` - Generate HTML page with n links (1-200 links, for testing crawlers)
- `GET /range/<numbytes>` - Support HTTP range requests for partial content (max 100KB, supports chunk_size and duration)

### Redirects
- `GET /redirect/<n>` - 302 redirect n times (supports absolute/relative query parameter)
- `GET /absolute-redirect/<n>` - 302 absolute redirect n times
- `GET /relative-redirect/<n>` - 302 relative redirect n times
- `GET|POST|PUT|DELETE|PATCH|TRACE /redirect-to` - Redirect to any URL with custom 3XX status code (requires url and status_code parameters)

### Images
- `GET /image` - Return image based on Accept header (supports PNG, JPEG, WebP, SVG)
- `GET /image/png` - Return a simple PNG image
- `GET /image/jpeg` - Return a simple JPEG image
- `GET /image/webp` - Return a simple WebP image
- `GET /image/svg` - Return a simple SVG image

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

# Set multiple cookies via query parameters (follow redirect)
curl -L -c cookies.txt "http://localhost:5000/cookies/set?session=abc123&user=john&theme=dark"

# Set specific cookie with URL path
curl -L -c cookies.txt http://localhost:5000/cookies/set/username/alice

# Set cookie with special characters (URL encoded)
curl -L -c cookies.txt "http://localhost:5000/cookies/set?message=hello%20world%21"

# Delete specific cookies
curl -L -c cookies.txt "http://localhost:5000/cookies/delete?session&user"

# Using POST to set cookies
curl -X POST -L -c cookies.txt "http://localhost:5000/cookies/set?api_key=secret123"

# Chain operations: set, view, delete, view
curl -c cookies.txt "http://localhost:5000/cookies/set?test=value" && \
curl -b cookies.txt http://localhost:5000/cookies && \
curl -c cookies.txt "http://localhost:5000/cookies/delete?test" && \
curl -b cookies.txt http://localhost:5000/cookies
```

### Testing custom response headers
```bash
# Set custom headers via query parameters
curl -i "http://localhost:5000/response-headers?X-Custom=test&Server=HTTPilot"

# Using POST method
curl -X POST -i "http://localhost:5000/response-headers?Cache-Control=no-cache"
```

### Testing response formats and encoding
```bash
# Get robots.txt file
curl http://localhost:5000/robots.txt

# Test compression formats (note: responses are automatically compressed)
curl -H "Accept-Encoding: gzip" http://localhost:5000/gzip
curl -H "Accept-Encoding: deflate" http://localhost:5000/deflate
curl -H "Accept-Encoding: br" http://localhost:5000/brotli

# Test with verbose output to see compression headers
curl -v -H "Accept-Encoding: gzip" http://localhost:5000/gzip
curl -v -H "Accept-Encoding: deflate" http://localhost:5000/deflate
curl -v -H "Accept-Encoding: br" http://localhost:5000/brotli

# Test UTF-8 encoding
curl http://localhost:5000/encoding/utf8

# Test decompression (pipe to file and check size)
curl -H "Accept-Encoding: gzip" http://localhost:5000/gzip > gzip_response.json
curl -H "Accept-Encoding: deflate" http://localhost:5000/deflate > deflate_response.json
curl -H "Accept-Encoding: br" http://localhost:5000/brotli > brotli_response.json
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

### Testing dynamic data and delayed responses
```bash
# Basic delay test (3 seconds)
curl http://localhost:5000/delay/3

# Test with timing measurement
time curl http://localhost:5000/delay/5

# Longer delay test (10 seconds)
curl http://localhost:5000/delay/10

# Maximum allowed delay (60 seconds)
curl http://localhost:5000/delay/60

# Test error handling (exceeds 60 second limit)
curl http://localhost:5000/delay/120

# JSON output shows timing details
curl -s http://localhost:5000/delay/2 | python -m json.tool
```

### Testing base64 encoding and decoding
```bash
# Encode text to base64
curl http://localhost:5000/base64/encoding/hello
curl "http://localhost:5000/base64/encoding/Hello%20World"

# Decode base64 text
curl http://localhost:5000/base64/decoding/aGVsbG8=
curl http://localhost:5000/base64/decoding/aGVsbG93b3JsZA==

# Test invalid base64 (returns error)
curl http://localhost:5000/base64/decoding/invalid-base64

# Chain encoding and decoding
original="test123"
encoded=$(curl -s "http://localhost:5000/base64/encoding/$original")
decoded=$(curl -s "http://localhost:5000/base64/decoding/$encoded")
echo "Original: $original, Encoded: $encoded, Decoded: $decoded"
```

### Testing random data generation
```bash
# Generate 100 random bytes and check size
curl http://localhost:5000/bytes/100 | wc -c

# Generate with seed for reproducible output
curl "http://localhost:5000/bytes/50?seed=12345" | hexdump -C
curl "http://localhost:5000/bytes/50?seed=12345" | hexdump -C  # Same output

# Generate different sizes
curl http://localhost:5000/bytes/1024 | wc -c     # 1KB
curl http://localhost:5000/bytes/10240 | wc -c    # 10KB

# Save to file for further testing
curl http://localhost:5000/bytes/500 -o random.bin
file random.bin
ls -la random.bin

# Test maximum size (1MB limit)
curl http://localhost:5000/bytes/1048576 | wc -c
```

### Testing UUID generation
```bash
# Generate a single UUID
curl http://localhost:5000/uuid

# Pretty print JSON response
curl -s http://localhost:5000/uuid | python -m json.tool

# Generate multiple UUIDs (each will be unique)
for i in {1..5}; do 
    curl -s http://localhost:5000/uuid | jq -r '.uuid'
done

# Extract just the UUID value
uuid=$(curl -s http://localhost:5000/uuid | jq -r '.uuid')
echo "Generated UUID: $uuid"
```

### Testing streaming data
```bash
# Stream 5 JSON responses
curl http://localhost:5000/stream/5

# Count streamed responses
curl -s http://localhost:5000/stream/10 | wc -l

# Process each JSON response as it arrives
curl -s http://localhost:5000/stream/3 | while read line; do
    echo "Received: $line"
    echo "$line" | jq .id
done

# Stream with maximum items (100)
curl http://localhost:5000/stream/100 | tail -5
```

### Testing streaming bytes
```bash
# Stream 1KB of random bytes
curl http://localhost:5000/stream-bytes/1024 | wc -c

# Stream with seed for reproducible output
curl "http://localhost:5000/stream-bytes/500?seed=42" | hexdump -C | head -10

# Stream with custom chunk size
curl "http://localhost:5000/stream-bytes/100?chunk_size=10" | wc -c

# Save streamed bytes to file
curl "http://localhost:5000/stream-bytes/2048?seed=123" -o stream.bin
ls -la stream.bin
file stream.bin

# Compare reproducible streams (should be identical)
curl "http://localhost:5000/stream-bytes/100?seed=999" > stream1.bin
curl "http://localhost:5000/stream-bytes/100?seed=999" > stream2.bin
diff stream1.bin stream2.bin  # Should show no differences

# Test maximum stream size (100KB)
curl http://localhost:5000/stream-bytes/102400 | wc -c
```

### Testing data dripping
```bash
# Basic drip (10 bytes over 2 seconds)
curl http://localhost:5000/drip

# Custom duration and bytes
curl "http://localhost:5000/drip?duration=5&numbytes=50"

# With initial delay
curl "http://localhost:5000/drip?delay=2&duration=3&numbytes=20"

# Measure timing
time curl "http://localhost:5000/drip?duration=4&numbytes=100"

# Large drip with custom status code
curl "http://localhost:5000/drip?duration=1&numbytes=1000&code=201"

# Test maximum size (10MB limit)
curl "http://localhost:5000/drip?duration=10&numbytes=10485760" | wc -c
```

### Testing link generation
```bash
# Generate page with 10 links
curl http://localhost:5000/links/10/0

# Different offset (highlights link 5)
curl http://localhost:5000/links/10/5

# Maximum links (200)
curl http://localhost:5000/links/200/0 | wc -l

# Extract all links from page
curl -s http://localhost:5000/links/5/2 | grep -o 'href="[^"]*"'

# Count links in page
curl -s http://localhost:5000/links/20/0 | grep -c '<a href='

# Test crawler behavior simulation
for i in {0..4}; do
    echo "Page $i:"
    curl -s "http://localhost:5000/links/5/$i" | grep -o "href='[^']*'" | head -3
done
```

### Testing HTTP range requests
```bash
# Full content (200 OK)
curl -i http://localhost:5000/range/100

# First 10 bytes (206 Partial Content)
curl -H "Range: bytes=0-9" -i http://localhost:5000/range/100
curl -H "Range: bytes=0-9" http://localhost:5000/range/100 | wc -c

# Last 10 bytes
curl -H "Range: bytes=-10" -i http://localhost:5000/range/100

# From byte 50 to end
curl -H "Range: bytes=50-" -i http://localhost:5000/range/100

# Middle section
curl -H "Range: bytes=20-29" -i http://localhost:5000/range/100

# Invalid range (416 Range Not Satisfiable)
curl -H "Range: bytes=200-300" -i http://localhost:5000/range/100

# Test with custom chunk size and duration
curl -H "Range: bytes=0-49" "http://localhost:5000/range/100?chunk_size=10&duration=2"

# Verify range content consistency
curl -H "Range: bytes=0-25" http://localhost:5000/range/100 > part1.txt
curl -H "Range: bytes=26-50" http://localhost:5000/range/100 > part2.txt
curl -H "Range: bytes=0-50" http://localhost:5000/range/100 > full.txt
cat part1.txt part2.txt > combined.txt
diff combined.txt full.txt  # Should be identical

# Test ETag and caching with ranges
curl -H "Range: bytes=0-9" -i http://localhost:5000/range/100 | grep -E "(ETag|Accept-Ranges|Content-Range)"
```

### Testing redirects
```bash
# Basic redirect test (3 redirects, follow automatically)
curl -L http://localhost:5000/redirect/3

# Test without following redirects (see Location header)
curl -i http://localhost:5000/redirect/1

# Force absolute redirects
curl -L "http://localhost:5000/redirect/2?absolute=true"

# Test absolute redirects endpoint
curl -L http://localhost:5000/absolute-redirect/2
curl -i http://localhost:5000/absolute-redirect/1

# Test relative redirects endpoint  
curl -L http://localhost:5000/relative-redirect/3
curl -i http://localhost:5000/relative-redirect/1

# Verbose output to see redirect chain
curl -v -L http://localhost:5000/redirect/2
curl -v -L http://localhost:5000/absolute-redirect/2
curl -v -L http://localhost:5000/relative-redirect/2

# Test custom redirect-to endpoint
curl -i "http://localhost:5000/redirect-to?url=http://example.com&status_code=302"
curl -i "http://localhost:5000/redirect-to?url=/ip&status_code=301"
curl -L "http://localhost:5000/redirect-to?url=/json&status_code=307"

# Test different HTTP methods with redirect-to
curl -X POST -i "http://localhost:5000/redirect-to?url=/post&status_code=303"
curl -X PUT -i "http://localhost:5000/redirect-to?url=/put&status_code=308"

# Test invalid parameters (returns 400 Bad Request)
curl -i "http://localhost:5000/redirect-to?url=test"  # missing status_code
curl -i "http://localhost:5000/redirect-to?status_code=302"  # missing url
curl -i "http://localhost:5000/redirect-to?url=test&status_code=invalid"  # invalid status_code

# Test redirect limits (most clients limit to ~20 redirects)
curl -L http://localhost:5000/redirect/5
```

### Testing images
```bash
# Get image based on Accept header (default: PNG)
curl "http://localhost:5000/image" -o downloaded_image.png

# Request specific image formats using Accept header
curl -H "Accept: image/jpeg" "http://localhost:5000/image" -o image.jpg
curl -H "Accept: image/webp" "http://localhost:5000/image" -o image.webp
curl -H "Accept: image/svg+xml" "http://localhost:5000/image" -o image.svg

# Request unsupported format (returns 406 Not Acceptable)
curl -i -H "Accept: image/gif" "http://localhost:5000/image"

# Get specific image formats directly
curl "http://localhost:5000/image/png" -o pig.png
curl "http://localhost:5000/image/jpeg" -o jackal.jpg
curl "http://localhost:5000/image/webp" -o wolf.webp
curl "http://localhost:5000/image/svg" -o logo.svg

# Check image headers and content type
curl -I "http://localhost:5000/image/png"
curl -I "http://localhost:5000/image/jpeg"
curl -I "http://localhost:5000/image/webp"
curl -I "http://localhost:5000/image/svg"

# View SVG image as text
curl "http://localhost:5000/image/svg"

# Test content negotiation with multiple Accept types
curl -H "Accept: image/webp,image/jpeg,*/*" "http://localhost:5000/image" -o negotiated.webp
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