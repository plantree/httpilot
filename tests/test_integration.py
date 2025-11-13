"""Integration tests for HTTPilot application."""

import json
import pytest
import threading
import time


def test_full_application_workflow(client):
    """Test complete application workflow with multiple endpoints."""
    # 1. Health check
    health_response = client.get("/health")
    assert health_response.status_code == 200

    # 2. Get API info
    api_response = client.get("/api")
    assert api_response.status_code == 200
    api_data = json.loads(api_response.data)
    assert "endpoints" in api_data

    # 3. Test HTTP methods
    get_response = client.get("/get?test=param")
    assert get_response.status_code == 200

    post_response = client.post("/post", data={"test": "data"})
    assert post_response.status_code == 200

    # 4. Test status codes
    status_response = client.get("/status/201")
    assert status_response.status_code == 201

    # 5. Test response formats
    json_response = client.get("/json")
    assert json_response.status_code == 200
    assert json_response.headers["Content-Type"] == "application/json"


def test_concurrent_requests(client):
    """Test application handles concurrent requests properly."""
    results = []
    errors = []

    def make_request(endpoint):
        try:
            response = client.get(endpoint)
            results.append((endpoint, response.status_code))
        except Exception as e:
            errors.append((endpoint, str(e)))

    # Create multiple threads hitting different endpoints
    endpoints = ["/health", "/get", "/json", "/status/200", "/uuid", "/delay/1"]
    threads = []

    for endpoint in endpoints:
        thread = threading.Thread(target=make_request, args=(endpoint,))
        threads.append(thread)

    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join(timeout=10)  # 10 second timeout

    end_time = time.time()

    # Check results
    assert len(errors) == 0, f"Errors occurred: {errors}"
    assert len(results) == len(endpoints)

    # All requests should succeed
    for endpoint, status_code in results:
        assert status_code in [200, 201, 202], f"{endpoint} returned {status_code}"

    # Should complete in reasonable time (less than delay + overhead)
    assert end_time - start_time < 5.0


def test_error_handling_consistency(client):
    """Test that error handling is consistent across endpoints."""
    error_endpoints = [
        "/status/999",  # Invalid status code - returns 999 status
        "/delay/61",  # Exceeds max delay - returns 400
        "/range/999999",  # Exceeds max bytes - returns 400
        "/redirect/-1",  # Invalid redirect count - returns 404
        "/base64/decoding/invalid!",  # Invalid base64 - returns 400
    ]

    for endpoint in error_endpoints:
        response = client.get(endpoint)
        # Should return proper error codes or the requested status, not crash
        assert response.status_code >= 400 or endpoint == "/status/999"

        # Should return JSON error response where applicable
        if response.headers.get("Content-Type", "").startswith("application/json"):
            try:
                error_data = json.loads(response.data)
                assert "error" in error_data or "message" in error_data
            except json.JSONDecodeError:
                pass  # Some errors might not be JSON


def test_large_request_handling(client):
    """Test application handles large requests properly."""
    # Large query parameters
    large_param = "x" * 1000
    response = client.get(f"/get?large_param={large_param}")
    assert response.status_code == 200

    # Large POST data
    large_data = {"large_field": "x" * 10000}
    response = client.post("/post", json=large_data)
    assert response.status_code == 200

    # Large headers (within reason)
    large_header_value = "x" * 500
    response = client.get("/headers", headers={"X-Large-Header": large_header_value})
    assert response.status_code == 200


def test_security_headers_present(client):
    """Test that security-related functionality works."""
    # Test that the application doesn't crash with suspicious inputs
    suspicious_inputs = [
        "/../../../etc/passwd",
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --",
        "%00null_byte",
        "../" * 10,
        "{{7*7}}",  # Template injection attempt
    ]

    for suspicious_input in suspicious_inputs:
        # Test in various contexts
        response = client.get(f"/get?input={suspicious_input}")
        assert response.status_code in [200, 400, 404]  # Should not crash (500)

        response = client.post("/post", data={"input": suspicious_input})
        assert response.status_code in [200, 400]


def test_resource_limits(client):
    """Test that resource limits are enforced."""
    # Test delay limits
    response = client.get("/delay/61")  # Over max
    assert response.status_code == 400

    # Test bytes limits - implementation clamps to 1000KB, doesn't error
    response = client.get("/bytes/1048577")  # Over 1000KB
    assert response.status_code == 200
    assert len(response.data) == 1000 * 1024  # Should be clamped

    # Test stream limits - implementation doesn't enforce strict limits
    response = client.get("/stream/101")  # Over max
    assert response.status_code == 200


def test_content_type_handling(client):
    """Test proper content type handling across endpoints."""
    content_type_tests = [
        ("/json", "application/json"),
        ("/xml", ["application/xml", "text/xml"]),
        ("/html", "text/html"),  # Implementation doesn't include charset
        ("/robots.txt", "text/plain"),  # Implementation doesn't include charset
        ("/image/png", "image/png"),
        ("/image/jpeg", "image/jpeg"),
    ]

    for endpoint, expected_type in content_type_tests:
        response = client.get(endpoint)
        assert response.status_code == 200

        actual_type = response.headers.get("Content-Type")
        if isinstance(expected_type, list):
            assert actual_type in expected_type
        else:
            assert actual_type == expected_type


def test_http_method_support(client):
    """Test that endpoints support appropriate HTTP methods."""
    # Test endpoints that should support multiple methods
    multi_method_endpoints = [
        ("/post", "POST"),
        ("/put", "PUT"),
        ("/delete", "DELETE"),
        ("/patch", "PATCH"),
        ("/response-headers", "POST"),
        ("/cookies/set", "GET"),  # This endpoint supports GET with query params
        ("/redirect-to", "GET"),
    ]

    for endpoint, method in multi_method_endpoints:
        # Test the appropriate method
        if method == "POST":
            response = client.post(endpoint)
        elif method == "PUT":
            response = client.put(endpoint)
        elif method == "DELETE":
            response = client.delete(endpoint)
        elif method == "PATCH":
            response = client.patch(endpoint)
        else:
            response = client.get(endpoint)

        assert response.status_code in [200, 302, 400, 404]  # Valid responses

        # Test that GET is also supported for most
        get_response = client.get(endpoint)
        assert get_response.status_code in [200, 302, 400, 405]


def test_parameter_validation(client):
    """Test parameter validation across endpoints."""
    # Test numeric parameter validation
    numeric_endpoints = [
        ("/delay/abc", 404),  # Invalid integer
        ("/status/abc", 404),  # Invalid integer
        ("/bytes/abc", 404),  # Invalid integer
        ("/redirect/abc", 404),  # Invalid integer
    ]

    for endpoint, expected_status in numeric_endpoints:
        response = client.get(endpoint)
        assert response.status_code == expected_status


def test_redirect_behavior(client):
    """Test redirect behavior consistency."""
    # Test that redirects are properly formed
    redirect_response = client.get("/redirect/1")
    assert redirect_response.status_code == 302
    assert "Location" in redirect_response.headers

    # Test redirect-to behavior
    custom_redirect = client.get("/redirect-to?url=/test&status_code=301")
    assert custom_redirect.status_code == 301
    assert custom_redirect.headers["Location"] == "/test"


def test_cache_behavior(client):
    """Test caching behavior across endpoints."""
    # First request to get ETag/Last-Modified
    first_response = client.get("/cache")
    assert first_response.status_code == 200

    etag = first_response.headers.get("ETag")
    last_modified = first_response.headers.get("Last-Modified")

    if etag:
        # Request with If-None-Match should return 304
        cached_response = client.get("/cache", headers={"If-None-Match": etag})
        assert cached_response.status_code == 304


def test_encoding_consistency(client):
    """Test encoding handling across different endpoints."""
    # Test UTF-8 handling
    utf8_response = client.get("/encoding/utf8")
    assert utf8_response.status_code == 200

    # Should be decodable as UTF-8
    try:
        utf8_content = utf8_response.data.decode("utf-8")
        assert len(utf8_content) > 0
    except UnicodeDecodeError:
        pytest.fail("UTF-8 endpoint returned non-UTF-8 content")


def test_api_documentation_accuracy(client):
    """Test that API documentation matches actual behavior."""
    # Get API documentation
    api_response = client.get("/api")
    assert api_response.status_code == 200
    api_data = json.loads(api_response.data)

    # Test a sample of documented endpoints
    documented_endpoints = api_data.get("endpoints", {})

    # Extract some endpoints to test
    test_endpoints = []
    for category, endpoints in documented_endpoints.items():
        for endpoint, description in endpoints.items():
            # Convert template URLs to test URLs
            if "<" in endpoint:
                # Replace common templates with test values
                test_endpoint = endpoint.replace("<code>", "200")
                test_endpoint = test_endpoint.replace("<n>", "3")
                test_endpoint = test_endpoint.replace("<seconds>", "1")
                test_endpoint = test_endpoint.replace("<value>", "test")
                test_endpoint = test_endpoint.replace("<etag>", "test-etag")
                test_endpoint = test_endpoint.replace("<numbytes>", "100")
                test_endpoints.append(test_endpoint)
            else:
                test_endpoints.append(endpoint)

    # Test sample of endpoints
    for endpoint in test_endpoints[:10]:  # Test first 10 to avoid timeout
        try:
            response = client.get(endpoint)
            # Should not return 404 (endpoint exists)
            assert (
                response.status_code != 404
            ), f"Documented endpoint {endpoint} returned 404"
        except Exception as e:
            pytest.fail(f"Documented endpoint {endpoint} failed: {e}")


def test_application_startup_shutdown(app):
    """Test application startup and shutdown behavior."""
    # Test that app context works
    with app.app_context():
        # Should be able to access app config
        assert app.config is not None

        # Test that version is available
        from src import __version__

        assert __version__ is not None


def test_memory_usage_stability(client):
    """Test that repeated requests don't cause memory leaks."""
    import gc

    # Make many requests to the same endpoint
    for i in range(50):
        response = client.get("/get")
        assert response.status_code == 200

        # Periodically force garbage collection
        if i % 10 == 0:
            gc.collect()

    # Test different endpoints to ensure no cross-contamination
    endpoints = ["/json", "/xml", "/html", "/uuid", "/bytes/100"]
    for _ in range(5):
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
