"""Tests for status code routes."""

import json
import pytest


def test_status_200(client):
    """Test 200 status code."""
    response = client.get('/status/200')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 200
    assert data['message'] == 'OK'


def test_status_404(client):
    """Test 404 status code."""
    response = client.get('/status/404')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 404
    assert data['message'] == 'Not Found'


def test_status_500(client):
    """Test 500 status code."""
    response = client.get('/status/500')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['status'] == 500
    assert data['message'] == 'Internal Server Error'


def test_status_418(client):
    """Test 418 I'm a teapot status code."""
    response = client.get('/status/418')
    assert response.status_code == 418
    data = json.loads(response.data)
    assert data['status'] == 418
    assert data['message'] == "I'm a teapot"


def test_status_204(client):
    """Test 204 No Content status code."""
    response = client.get('/status/204')
    assert response.status_code == 204
    assert len(response.data) == 0  # No content should be returned


def test_status_redirect(client):
    """Test redirect status codes."""
    response = client.get('/status/301')
    assert response.status_code == 301
    assert 'Location' in response.headers
    data = json.loads(response.data)
    assert data['status'] == 301
    assert data['message'] == 'Moved Permanently'


def test_random_status(client):
    """Test random status endpoint."""
    response = client.get('/status/random')
    assert response.status_code in [200, 201, 400, 401, 403, 404, 500, 502, 503]