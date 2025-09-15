"""Tests for basic application functionality."""

import json
import pytest


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'HTTPilot is running' in data['message']


def test_api_info(client):
    """Test API info endpoint."""
    response = client.get('/api')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'HTTPilot'
    assert data['version'] == '0.1.0'
    assert 'endpoints' in data


def test_index_page(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'HTTPilot' in response.data
    assert b'HTTP Testing Tool' in response.data


def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Not Found'
    assert data['status'] == 404