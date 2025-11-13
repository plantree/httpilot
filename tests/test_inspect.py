"""Tests for request inspection routes."""

import json
import pytest


def test_headers_endpoint(client):
    """Test headers inspection endpoint."""
    custom_headers = {
        "Custom-Header": "test-value",
        "X-API-Key": "secret-key",
        "User-Agent": "Test-Agent/1.0",
    }

    response = client.get("/headers", headers=custom_headers)
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "headers" in data
    assert isinstance(data["headers"], dict)

    # Check that our custom headers appear in the response
    response_headers = data["headers"]
    assert response_headers.get("Custom-Header") == "test-value"
    assert (
        response_headers.get("X-Api-Key") == "secret-key"
    )  # Flask normalizes header case
    assert response_headers.get("User-Agent") == "Test-Agent/1.0"


def test_headers_endpoint_no_custom_headers(client):
    """Test headers endpoint without custom headers."""
    response = client.get("/headers")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "headers" in data
    assert isinstance(data["headers"], dict)
    # Should still have default headers like Host, etc.
    assert len(data["headers"]) > 0


def test_headers_endpoint_multiple_values(client):
    """Test headers endpoint with multiple header values."""
    # Flask test client may not support multiple headers with same name easily
    # This tests the basic functionality
    response = client.get("/headers", headers={"Accept": "application/json, text/html"})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "headers" in data
    accept_header = data["headers"].get("Accept")
    assert accept_header is not None


def test_ip_endpoint(client):
    """Test IP address inspection endpoint."""
    response = client.get("/ip")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "origin" in data
    assert isinstance(data["origin"], str)
    # In test environment, likely to be 127.0.0.1 or similar
    assert len(data["origin"]) > 0


def test_ip_endpoint_with_forwarded_headers(client):
    """Test IP endpoint with X-Forwarded-For header."""
    forwarded_ip = "192.168.1.100"
    response = client.get("/ip", headers={"X-Forwarded-For": forwarded_ip})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "origin" in data
    # Behavior depends on implementation - might use forwarded IP or original


def test_ip_endpoint_with_real_ip_header(client):
    """Test IP endpoint with X-Real-IP header."""
    real_ip = "10.0.0.1"
    response = client.get("/ip", headers={"X-Real-IP": real_ip})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "origin" in data


def test_user_agent_endpoint(client):
    """Test user agent inspection endpoint."""
    test_user_agent = "Mozilla/5.0 (Test Browser) HTTPilot/1.0"
    response = client.get("/user-agent", headers={"User-Agent": test_user_agent})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "user-agent" in data
    assert data["user-agent"] == test_user_agent


def test_user_agent_endpoint_no_header(client):
    """Test user agent endpoint without User-Agent header."""
    response = client.get("/user-agent")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "user-agent" in data
    # Should be None or default value when no User-Agent provided
    user_agent = data["user-agent"]
    assert user_agent is None or isinstance(user_agent, str)


def test_user_agent_endpoint_empty_header(client):
    """Test user agent endpoint with empty User-Agent header."""
    response = client.get("/user-agent", headers={"User-Agent": ""})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "user-agent" in data
    assert data["user-agent"] == ""


def test_user_agent_endpoint_long_header(client):
    """Test user agent endpoint with very long User-Agent."""
    long_user_agent = "A" * 1000  # 1KB user agent
    response = client.get("/user-agent", headers={"User-Agent": long_user_agent})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "user-agent" in data
    assert data["user-agent"] == long_user_agent


def test_user_agent_endpoint_special_characters(client):
    """Test user agent endpoint with special characters."""
    special_user_agent = "Mozilla/5.0 (Test; 中文; русский) WebKit/537.36"
    response = client.get("/user-agent", headers={"User-Agent": special_user_agent})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "user-agent" in data
    assert data["user-agent"] == special_user_agent


def test_headers_endpoint_case_sensitivity(client):
    """Test headers endpoint handles case sensitivity properly."""
    mixed_case_headers = {
        "Content-Type": "application/json",
        "content-type": "text/plain",  # Duplicate with different case
        "X-Custom-Header": "value1",
        "x-custom-header": "value2",  # Duplicate with different case
    }

    response = client.get("/headers", headers=mixed_case_headers)
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "headers" in data
    # Flask/Werkzeug normalizes headers, so we test that it handles them


def test_headers_endpoint_security_headers(client):
    """Test headers endpoint with security-related headers."""
    security_headers = {
        "Authorization": "Bearer token123",
        "X-API-Key": "secret-key",
        "X-CSRF-Token": "csrf-token-456",
    }

    response = client.get("/headers", headers=security_headers)
    assert response.status_code == 200
    data = json.loads(response.data)

    # Should reflect all headers (this endpoint is for inspection)
    response_headers = data["headers"]
    assert "Authorization" in response_headers
    assert "X-Api-Key" in response_headers  # Flask normalizes case


def test_ip_endpoint_json_format(client):
    """Test IP endpoint returns properly formatted JSON."""
    response = client.get("/ip")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Should be valid JSON
    try:
        data = json.loads(response.data)
        assert isinstance(data, dict)
    except json.JSONDecodeError:
        pytest.fail("IP endpoint did not return valid JSON")


def test_headers_endpoint_json_format(client):
    """Test headers endpoint returns properly formatted JSON."""
    response = client.get("/headers")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    try:
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert isinstance(data["headers"], dict)
    except json.JSONDecodeError:
        pytest.fail("Headers endpoint did not return valid JSON")


def test_user_agent_endpoint_json_format(client):
    """Test user agent endpoint returns properly formatted JSON."""
    response = client.get("/user-agent")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    try:
        data = json.loads(response.data)
        assert isinstance(data, dict)
    except json.JSONDecodeError:
        pytest.fail("User-Agent endpoint did not return valid JSON")


def test_request_inspection_consistency(client):
    """Test that request inspection endpoints are consistent."""
    # All inspection endpoints should return JSON
    endpoints = ["/headers", "/ip", "/user-agent"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        data = json.loads(response.data)
        assert isinstance(data, dict)


def test_headers_with_binary_content(client):
    """Test headers endpoint with binary content in headers."""
    # Some proxies or clients might send binary data in headers
    import base64

    binary_data = b"\x00\x01\x02\x03"
    encoded_data = base64.b64encode(binary_data).decode("ascii")

    response = client.get("/headers", headers={"X-Binary": encoded_data})
    assert response.status_code == 200
    data = json.loads(response.data)

    # Should handle binary data gracefully
    assert "headers" in data
