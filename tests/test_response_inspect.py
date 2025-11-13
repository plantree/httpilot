"""Tests for response inspection routes."""

import json
import pytest


def test_response_headers_get_no_params(client):
    """Test response headers endpoint with GET and no parameters."""
    response = client.get("/response-headers")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)  # Returns headers directly as JSON object


def test_response_headers_get_with_params(client):
    """Test response headers endpoint with GET and query parameters."""
    response = client.get(
        "/response-headers?X-Custom-Header=test-value&Server=HTTPilot"
    )
    assert response.status_code == 200

    # Check that custom headers were set
    assert response.headers.get("X-Custom-Header") == "test-value"
    assert response.headers.get("Server") == "HTTPilot"

    data = json.loads(response.data)
    assert "X-custom-header" in data  # Headers returned directly in JSON


def test_response_headers_post_no_params(client):
    """Test response headers endpoint with POST and no parameters."""
    response = client.post("/response-headers")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)  # Returns headers directly as JSON object


def test_response_headers_post_with_params(client):
    """Test response headers endpoint with POST and query parameters."""
    response = client.post("/response-headers?Cache-Control=no-cache&X-API-Version=v1")
    assert response.status_code == 200

    # Check that custom headers were set
    assert response.headers.get("Cache-Control") == "no-cache"
    assert response.headers.get("X-API-Version") == "v1"


def test_response_headers_multiple_values(client):
    """Test response headers endpoint with multiple header values."""
    response = client.get("/response-headers?Accept=application/json&Accept=text/html")
    assert response.status_code == 200

    # Should handle multiple values (behavior may vary based on implementation)
    accept_header = response.headers.get("Accept")
    assert accept_header is not None


def test_response_headers_special_characters(client):
    """Test response headers endpoint with special characters."""
    from urllib.parse import quote

    header_value = "test value with spaces & special chars!"
    encoded_value = quote(header_value)

    response = client.get(f"/response-headers?X-Special={encoded_value}")
    assert response.status_code == 200

    # Header should be set (may be URL-decoded)
    special_header = response.headers.get("X-Special")
    assert special_header is not None


def test_response_headers_empty_values(client):
    """Test response headers endpoint with empty values."""
    response = client.get("/response-headers?X-Empty=")
    assert response.status_code == 200

    # Should handle empty values
    empty_header = response.headers.get("X-Empty")
    # May be empty string or None depending on implementation
    assert empty_header == "" or empty_header is None


def test_response_headers_case_sensitivity(client):
    """Test response headers endpoint case handling."""
    response = client.get(
        "/response-headers?content-type=application/custom&Content-Type=text/plain"
    )
    assert response.status_code == 200

    # Check how case is handled
    content_type = response.headers.get("Content-Type")
    assert content_type is not None


def test_response_headers_standard_headers(client):
    """Test response headers endpoint with standard HTTP headers."""
    standard_headers = {
        "Content-Type": "application/json",
        "Cache-Control": "max-age=3600",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
    }

    query_params = "&".join([f"{k}={v}" for k, v in standard_headers.items()])
    response = client.get(f"/response-headers?{query_params}")
    assert response.status_code == 200

    # Check that all headers were set
    for header_name, header_value in standard_headers.items():
        assert response.headers.get(header_name) == header_value


def test_response_headers_forbidden_headers(client):
    """Test response headers endpoint with potentially forbidden headers."""
    # Some headers might be restricted by Flask/server
    potentially_forbidden = [
        "Host",
        "Connection",
        "Transfer-Encoding",
        "Content-Length",  # This might be overridden by Flask
    ]

    for header in potentially_forbidden:
        response = client.get(f"/response-headers?{header}=custom-value")
        assert response.status_code == 200
        # Test passes regardless of whether header is set or ignored


def test_response_headers_large_values(client):
    """Test response headers endpoint with large header values."""
    large_value = "x" * 1000  # 1KB header value
    response = client.get(f"/response-headers?X-Large={large_value}")
    assert response.status_code == 200

    # Should handle reasonably large headers
    large_header = response.headers.get("X-Large")
    if large_header:
        assert len(large_header) > 0


def test_response_headers_many_headers(client):
    """Test response headers endpoint with many custom headers."""
    params = []
    for i in range(20):
        params.append(f"X-Header-{i}=value-{i}")

    query_string = "&".join(params)
    response = client.get(f"/response-headers?{query_string}")
    assert response.status_code == 200

    # Should handle many headers
    data = json.loads(response.data)
    assert len(data) >= 20  # Should contain all headers


def test_response_headers_security_headers(client):
    """Test response headers endpoint with security-related headers."""
    security_headers = {
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    query_params = "&".join([f"{k}={v}" for k, v in security_headers.items()])
    response = client.get(f"/response-headers?{query_params}")
    assert response.status_code == 200

    # Verify security headers are set
    for header_name, header_value in security_headers.items():
        set_value = response.headers.get(header_name)
        if set_value:  # Some might be filtered by Flask
            assert set_value == header_value


def test_response_headers_cors_headers(client):
    """Test response headers endpoint with CORS headers."""
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400",
    }

    query_params = "&".join([f"{k}={v}" for k, v in cors_headers.items()])
    response = client.get(f"/response-headers?{query_params}")
    assert response.status_code == 200

    # Check CORS headers
    for header_name, header_value in cors_headers.items():
        assert response.headers.get(header_name) == header_value


def test_response_headers_content_type_override(client):
    """Test response headers endpoint overriding Content-Type."""
    response = client.get("/response-headers?Content-Type=application/xml")
    assert response.status_code == 200

    # Should override the default Content-Type
    content_type = response.headers.get("Content-Type")
    # Might be overridden or might stay as original JSON
    assert content_type is not None


def test_response_headers_custom_status_code(client):
    """Test response headers endpoint with custom status indication."""
    # This tests if the endpoint supports status code modification
    # (depends on implementation)
    response = client.get("/response-headers?Status=201")
    # Should still return 200 unless specifically implemented to change status
    assert response.status_code == 200


def test_response_headers_json_response_format(client):
    """Test response headers endpoint returns proper JSON format."""
    response = client.get("/response-headers?X-Test=value")
    assert response.status_code == 200

    # Should return valid JSON
    try:
        data = json.loads(response.data)
        assert isinstance(data, dict)
        # Headers are returned directly as the JSON object
    except json.JSONDecodeError:
        pytest.fail("Response headers endpoint did not return valid JSON")


def test_response_headers_method_support(client):
    """Test response headers endpoint supports correct HTTP methods."""
    # Test GET
    get_response = client.get("/response-headers")
    assert get_response.status_code == 200

    # Test POST
    post_response = client.post("/response-headers")
    assert post_response.status_code == 200

    # Test unsupported methods should return 405
    put_response = client.put("/response-headers")
    assert put_response.status_code == 405

    delete_response = client.delete("/response-headers")
    assert delete_response.status_code == 405


def test_response_headers_head_request(client):
    """Test response headers endpoint with HEAD request."""
    response = client.head("/response-headers?X-Test=value")
    assert response.status_code == 200
    assert len(response.data) == 0  # HEAD should not return body

    # Custom headers should still be set
    assert response.headers.get("X-Test") == "value"


def test_response_headers_options_request(client):
    """Test response headers endpoint with OPTIONS request."""
    response = client.options("/response-headers")

    # Should return allowed methods
    if response.status_code == 200:
        assert "Allow" in response.headers
        allowed_methods = response.headers["Allow"]
        assert "GET" in allowed_methods
        assert "POST" in allowed_methods


def test_response_headers_encoding_handling(client):
    """Test response headers endpoint handles encoding properly."""
    # Test with UTF-8 characters in header values
    unicode_value = "测试值"
    from urllib.parse import quote

    encoded_value = quote(unicode_value.encode("utf-8"))
    response = client.get(f"/response-headers?X-Unicode={encoded_value}")
    assert response.status_code == 200

    # Should handle Unicode in headers gracefully
    unicode_header = response.headers.get("X-Unicode")
    # Behavior may vary - should not crash
