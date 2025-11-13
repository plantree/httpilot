"""Tests for cookie routes."""

import json
import pytest
from urllib.parse import quote


def test_get_cookies_no_cookies(client):
    """Test getting cookies when none are sent."""
    response = client.get("/cookies")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "cookies" in data
    assert data["cookies"] == {}


def test_get_cookies_with_cookies(client):
    """Test getting cookies when cookies are sent."""
    # Set cookies using the test client
    client.set_cookie("localhost", "test", "value")
    client.set_cookie("localhost", "session", "abc123")

    response = client.get("/cookies")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "cookies" in data
    assert data["cookies"]["test"] == "value"
    assert data["cookies"]["session"] == "abc123"


def test_add_random_cookies(client):
    """Test endpoint that doesn't exist - should return 404."""
    response = client.get("/cookies/add")
    assert response.status_code == 404


def test_clear_cookies(client):
    """Test endpoint that doesn't exist - should return 404."""
    response = client.get("/cookies/clear")
    assert response.status_code == 404


def test_set_cookies_from_query_params_get(client):
    """Test setting cookies from query parameters using GET."""
    response = client.get("/cookies/set?session=abc123&user=john&theme=dark")
    assert response.status_code == 302  # Should redirect
    assert response.headers.get("Location").endswith("/cookies")

    # Check Set-Cookie headers
    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 3

    cookie_values = {}
    for cookie in set_cookies:
        parts = cookie.split(";")[0].split("=", 1)
        cookie_values[parts[0]] = parts[1]

    assert cookie_values["session"] == "abc123"
    assert cookie_values["user"] == "john"
    assert cookie_values["theme"] == "dark"


def test_set_cookies_from_query_params_post(client):
    """Test POST method not supported - should return 405."""
    response = client.post("/cookies/set?api_key=secret123&role=admin")
    assert response.status_code == 405  # Method not allowed


def test_set_cookies_no_params(client):
    """Test setting cookies with no query parameters."""
    response = client.get("/cookies/set")
    assert response.status_code == 302
    assert response.headers.get("Location").endswith("/cookies")

    # Should not set any cookies
    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 0


def test_set_cookie_specific_name_value_get(client):
    """Test setting specific cookie with name and value using GET."""
    response = client.get("/cookies/set/username/alice")
    assert response.status_code == 302
    assert response.headers.get("Location").endswith("/cookies")

    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 1
    assert set_cookies[0].startswith("username=alice")


def test_set_cookie_specific_name_value_post(client):
    """Test POST method not supported - should return 405."""
    response = client.post("/cookies/set/token/xyz789")
    assert response.status_code == 405  # Method not allowed


def test_set_cookie_with_special_characters(client):
    """Test setting cookie with URL-encoded special characters."""
    encoded_value = quote("hello world!")
    response = client.get(f"/cookies/set/message/{encoded_value}")
    assert response.status_code == 302

    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 1
    # Flask automatically URL-decodes the path parameter
    assert "message=" in set_cookies[0]


def test_delete_cookies_get(client):
    """Test deleting cookies using GET."""
    response = client.get("/cookies/delete?session&user&theme")
    assert response.status_code == 302
    assert response.headers.get("Location").endswith("/cookies")

    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 3

    # All cookies should be expired
    for cookie in set_cookies:
        assert "max-age=0" in cookie.lower()
        # Check cookie names
        cookie_name = cookie.split("=")[0]
        assert cookie_name in ["session", "user", "theme"]


def test_delete_cookies_post(client):
    """Test POST method not supported - should return 405."""
    response = client.post("/cookies/delete?api_key&token")
    assert response.status_code == 405  # Method not allowed


def test_delete_cookies_no_params(client):
    """Test deleting cookies with no parameters."""
    response = client.get("/cookies/delete")
    assert response.status_code == 302

    # Should not delete any cookies
    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 0


def test_delete_cookies_with_values(client):
    """Test deleting cookies ignores parameter values."""
    response = client.get("/cookies/delete?session=ignored&user=alsoingnored")
    assert response.status_code == 302

    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 2

    # Should delete both cookies regardless of values
    cookie_names = [cookie.split("=")[0] for cookie in set_cookies]
    assert "session" in cookie_names
    assert "user" in cookie_names


def test_cookie_security_attributes(client):
    """Test that cookies include security attributes when appropriate."""
    response = client.get("/cookies/set/secure_test/value")
    assert response.status_code == 302

    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 1

    cookie = set_cookies[0]
    # Check basic cookie structure
    assert "secure_test=value" in cookie
    assert "Path=/" in cookie


def test_cookie_workflow_integration(client):
    """Test complete cookie workflow: set -> view -> delete -> view."""
    # Set cookies
    response = client.get("/cookies/set?test=value&another=data")
    assert response.status_code == 302

    # Follow redirect would require manual cookie handling in tests
    # This tests the redirect response itself
    location = response.headers.get("Location")
    assert location.endswith("/cookies")

    # Verify cookies were set
    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 2


def test_multiple_cookie_operations(client):
    """Test multiple cookie operations in sequence."""
    # Set multiple cookies
    response1 = client.get("/cookies/set/first/value1")
    assert response1.status_code == 302

    response2 = client.get("/cookies/set/second/value2")
    assert response2.status_code == 302

    # Delete one cookie
    response3 = client.get("/cookies/delete?first")
    assert response3.status_code == 302

    # Each operation should work independently
    for response in [response1, response2, response3]:
        assert response.headers.get("Location").endswith("/cookies")


def test_cookie_name_validation(client):
    """Test cookie name and value handling."""
    # Test with valid cookie name and value
    response = client.get("/cookies/set/valid_name123/valid_value456")
    assert response.status_code == 302

    set_cookies = response.headers.getlist("Set-Cookie")
    assert len(set_cookies) == 1
    assert "valid_name123=valid_value456" in set_cookies[0]


def test_empty_cookie_value(client):
    """Test setting cookie with empty value."""
    response = client.get("/cookies/set/empty_test/")
    # Flask route requires a value, empty path segment results in 404
    assert response.status_code == 404
