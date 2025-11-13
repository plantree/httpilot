"""Tests for cache routes."""

import json
import pytest
from datetime import datetime, timezone


def test_cache_no_headers(client):
    """Test cache endpoint without conditional headers."""
    response = client.get("/cache")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "Returns with no cache"
    assert "Last-Modified" in response.headers
    assert "ETag" in response.headers


def test_cache_with_if_modified_since(client):
    """Test cache with If-Modified-Since header (should return 304)."""
    # First request to get Last-Modified
    response = client.get("/cache")
    last_modified = response.headers.get("Last-Modified")

    # Second request with If-Modified-Since
    response = client.get("/cache", headers={"If-Modified-Since": last_modified})
    assert response.status_code == 304
    assert len(response.data) == 0


def test_cache_with_if_none_match(client):
    """Test cache with If-None-Match header (should return 304)."""
    # First request to get ETag
    response = client.get("/cache")
    etag = response.headers.get("ETag")

    # Second request with If-None-Match
    response = client.get("/cache", headers={"If-None-Match": etag})
    assert response.status_code == 304
    assert len(response.data) == 0


def test_cache_with_seconds(client):
    """Test cache endpoint with seconds parameter."""
    response = client.get("/cache/300")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "Cache will be valid for 300 seconds" in data["message"]
    assert "Cache-Control" in response.headers
    assert "max-age=300" in response.headers["Cache-Control"]


def test_cache_with_zero_seconds(client):
    """Test cache endpoint with zero seconds."""
    response = client.get("/cache/0")
    assert response.status_code == 200
    assert "Cache-Control" in response.headers
    assert "max-age=0" in response.headers["Cache-Control"]


def test_etag_endpoint(client):
    """Test ETag endpoint."""
    test_etag = "test-etag-123"
    response = client.get(f"/etag/{test_etag}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert response.headers.get("ETag") == test_etag


def test_etag_with_if_none_match_matching(client):
    """Test ETag endpoint with matching If-None-Match (should return 304)."""
    test_etag = "test-etag-456"
    response = client.get(
        f"/etag/{test_etag}", headers={"If-None-Match": f'"{test_etag}"'}
    )
    assert response.status_code == 304
    assert len(response.data) == 0


def test_etag_with_if_none_match_not_matching(client):
    """Test ETag endpoint with non-matching If-None-Match (should return 200)."""
    test_etag = "test-etag-def"
    response = client.get(
        f"/etag/{test_etag}", headers={"If-None-Match": '"different-etag"'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert response.headers["ETag"] == test_etag


def test_etag_with_if_match_matching(client):
    """Test ETag endpoint with matching If-Match (should return 200)."""
    test_etag = "test-etag-abc"
    response = client.get(f"/etag/{test_etag}", headers={"If-Match": f'"{test_etag}"'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data


def test_etag_with_if_match_not_matching(client):
    """Test ETag endpoint with non-matching If-Match (should return 412)."""
    test_etag = "test-etag-abc"
    response = client.get(
        f"/etag/{test_etag}", headers={"If-Match": '"different-etag"'}
    )
    assert response.status_code == 412  # Precondition Failed
    # 412 response has no body, just status code


def test_etag_with_if_match_wildcard(client):
    """Test ETag endpoint with wildcard If-Match (should return 200)."""
    test_etag = "test-etag-wildcard"
    response = client.get(f"/etag/{test_etag}", headers={"If-Match": "*"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert response.headers["ETag"] == test_etag


def test_etag_with_weak_etag(client):
    """Test ETag endpoint with weak ETag."""
    test_etag = "weak-etag"
    response = client.get(
        f"/etag/{test_etag}", headers={"If-None-Match": f'W/"{test_etag}"'}
    )
    # Should still match for weak comparison
    assert response.status_code == 304


def test_cache_headers_format(client):
    """Test cache headers are properly formatted."""
    response = client.get("/cache")
    assert response.status_code == 200

    # Check Last-Modified format (RFC 7234)
    last_modified = response.headers.get("Last-Modified")
    assert last_modified is not None

    # Check ETag format (UUID hex without quotes in this implementation)
    etag = response.headers.get("ETag")
    assert etag is not None
    assert len(etag) == 32  # UUID hex string length


def test_cache_multiple_conditions(client):
    """Test cache with multiple conditional headers."""
    # First request to get both headers
    response = client.get("/cache")
    last_modified = response.headers.get("Last-Modified")
    etag = response.headers.get("ETag")

    # Request with both conditions (should return 304)
    response = client.get(
        "/cache", headers={"If-Modified-Since": last_modified, "If-None-Match": etag}
    )
    assert response.status_code == 304
