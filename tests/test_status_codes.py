"""Tests for status code routes."""

import json
import pytest


def test_status_200(client):
    """Test 200 status code."""
    response = client.get("/status/200")
    assert response.status_code == 200
    # Status 200 returns empty response by default


def test_status_404(client):
    """Test 404 status code."""
    response = client.get("/status/404")
    assert response.status_code == 404
    # Status 404 returns empty response by default


def test_status_500(client):
    """Test 500 status code."""
    response = client.get("/status/500")
    assert response.status_code == 500
    # Status 500 returns empty response by default


def test_status_418(client):
    """Test 418 I'm a teapot status code."""
    response = client.get("/status/418")
    assert response.status_code == 418
    # Status 418 returns ASCII art teapot (text content)
    assert "teapot" in response.data.decode("utf-8")


def test_status_204(client):
    """Test 204 No Content status code."""
    response = client.get("/status/204")
    assert response.status_code == 204
    assert len(response.data) == 0  # No content should be returned


def test_status_redirect(client):
    """Test redirect status codes."""
    response = client.get("/status/301")
    assert response.status_code == 301
    assert "Location" in response.headers
    # Redirect status returns empty response by default


def test_random_status(client):
    """Test random status endpoint."""
    response = client.get("/status/random")
    assert response.status_code in [200, 201, 400, 401, 403, 404, 500, 502, 503]
