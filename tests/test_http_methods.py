"""Tests for HTTP methods routes."""

import json
import pytest


def test_get_method(client):
    """Test GET method endpoint."""
    response = client.get('/get?param1=value1&param2=value2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['method'] == 'GET'
    assert data['args']['param1'] == 'value1'
    assert data['args']['param2'] == 'value2'
    assert 'headers' in data
    assert 'timestamp' in data


def test_post_method_json(client):
    """Test POST method with JSON data."""
    test_data = {'key': 'value', 'number': 42}
    response = client.post('/post', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['method'] == 'POST'
    assert data['json'] == test_data
    assert 'headers' in data


def test_post_method_form(client):
    """Test POST method with form data."""
    form_data = {'field1': 'value1', 'field2': 'value2'}
    response = client.post('/post', data=form_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['method'] == 'POST'
    assert data['form'] == form_data


def test_put_method(client):
    """Test PUT method."""
    test_data = {'update': 'data'}
    response = client.put('/put',
                         data=json.dumps(test_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['method'] == 'PUT'
    assert data['json'] == test_data


def test_delete_method(client):
    """Test DELETE method."""
    response = client.delete('/delete')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['method'] == 'DELETE'


def test_patch_method(client):
    """Test PATCH method."""
    test_data = {'patch': 'data'}
    response = client.patch('/patch',
                           data=json.dumps(test_data),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['method'] == 'PATCH'
    assert data['json'] == test_data


def test_head_method(client):
    """Test HEAD method."""
    response = client.head('/head')
    assert response.status_code == 200
    assert len(response.data) == 0  # HEAD should not return body


def test_options_method(client):
    """Test OPTIONS method."""
    response = client.options('/options')
    assert response.status_code == 200
    assert 'Allow' in response.headers
    data = json.loads(response.data)
    assert data['method'] == 'OPTIONS'