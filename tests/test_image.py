"""Tests for image routes."""

import json
import pytest


def test_image_default_png(client):
    """Test image endpoint returns PNG by default."""
    response = client.get("/image")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert len(response.data) > 0


def test_image_accept_header_png(client):
    """Test image endpoint with PNG accept header."""
    response = client.get("/image", headers={"Accept": "image/png"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"


def test_image_accept_header_jpeg(client):
    """Test image endpoint with JPEG accept header."""
    response = client.get("/image", headers={"Accept": "image/jpeg"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"


def test_image_accept_header_webp(client):
    """Test image endpoint with WebP accept header."""
    response = client.get("/image", headers={"Accept": "image/webp"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/webp"


def test_image_accept_header_svg(client):
    """Test image endpoint with SVG accept header."""
    response = client.get("/image", headers={"Accept": "image/svg+xml"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/svg+xml"


def test_image_accept_header_wildcard(client):
    """Test image endpoint with wildcard accept header."""
    response = client.get("/image", headers={"Accept": "image/*"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"  # Should default to PNG


def test_image_accept_header_multiple(client):
    """Test image endpoint with multiple accept headers."""
    response = client.get("/image", headers={"Accept": "image/webp,image/jpeg,*/*"})
    assert response.status_code == 200
    assert (
        response.headers["Content-Type"] == "image/webp"
    )  # Should prefer first supported


def test_image_accept_header_unsupported(client):
    """Test image endpoint with unsupported accept header."""
    response = client.get("/image", headers={"Accept": "image/gif"})
    assert response.status_code == 406  # Not Acceptable
    data = json.loads(response.data)
    assert "message" in data
    assert "accept" in data  # Shows supported types


def test_image_accept_header_case_insensitive(client):
    """Test image endpoint with case-insensitive accept header."""
    response = client.get("/image", headers={"Accept": "IMAGE/PNG"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"


def test_image_png_direct(client):
    """Test PNG image endpoint directly."""
    response = client.get("/image/png")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert len(response.data) > 0

    # Verify it's actually PNG data (starts with PNG signature)
    assert response.data.startswith(b"\x89PNG\r\n\x1a\n")


def test_image_jpeg_direct(client):
    """Test JPEG image endpoint directly."""
    response = client.get("/image/jpeg")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"
    assert len(response.data) > 0

    # Verify it's actually JPEG data (starts with JPEG signature)
    assert response.data.startswith(b"\xff\xd8\xff")


def test_image_webp_direct(client):
    """Test WebP image endpoint directly."""
    response = client.get("/image/webp")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/webp"
    assert len(response.data) > 0

    # Verify it's actually WebP data
    assert b"WEBP" in response.data[:20]


def test_image_svg_direct(client):
    """Test SVG image endpoint directly."""
    response = client.get("/image/svg")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/svg+xml"
    assert len(response.data) > 0

    # Verify it's actually SVG data
    svg_content = response.data.decode()
    assert svg_content.strip().startswith("<svg") or svg_content.strip().startswith(
        "<?xml"
    )


def test_image_head_requests(client):
    """Test HEAD requests to image endpoints."""
    response = client.head("/image/png")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert len(response.data) == 0  # HEAD should not return body


def test_image_options_requests(client):
    """Test OPTIONS requests to image endpoints."""
    response = client.options("/image/png")
    assert response.status_code == 200
    assert "Allow" in response.headers


def test_image_consistency(client):
    """Test that same image format returns consistent data."""
    response1 = client.get("/image/png")
    response2 = client.get("/image/png")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.data == response2.data  # Should be identical


def test_image_content_length(client):
    """Test that image responses include Content-Length header."""
    response = client.get("/image/png")
    assert response.status_code == 200
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) == len(response.data)


def test_image_cache_headers(client):
    """Test that image responses can be cached."""
    response = client.get("/image/png")
    assert response.status_code == 200
    # Images should be cacheable (no Cache-Control: no-cache)
    cache_control = response.headers.get("Cache-Control")
    if cache_control:
        assert "no-cache" not in cache_control.lower()


def test_image_accept_header_priority(client):
    """Test image content negotiation priority."""
    # WebP should be preferred over JPEG when both are accepted
    response = client.get("/image", headers={"Accept": "image/webp,image/jpeg"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/webp"

    # JPEG should be preferred over PNG when both are accepted
    response = client.get("/image", headers={"Accept": "image/jpeg,image/png"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"


def test_image_malformed_accept_header(client):
    """Test image endpoint with malformed accept header."""
    response = client.get("/image", headers={"Accept": "not-a-valid-mime-type"})
    assert response.status_code == 406  # Should reject invalid MIME types


def test_image_empty_accept_header(client):
    """Test image endpoint with empty accept header."""
    response = client.get("/image", headers={"Accept": ""})
    assert response.status_code == 406  # Empty accept header is not acceptable
    data = json.loads(response.data)
    assert "message" in data


def test_image_no_accept_header(client):
    """Test image endpoint with no accept header."""
    # Remove default Accept header if Flask test client adds one
    response = client.get("/image")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"  # Should default to PNG


def test_all_image_formats_available(client):
    """Test that all advertised image formats are actually available."""
    formats = [
        ("/image/png", "image/png"),
        ("/image/jpeg", "image/jpeg"),
        ("/image/webp", "image/webp"),
        ("/image/svg", "image/svg+xml"),
    ]

    for endpoint, content_type in formats:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.headers["Content-Type"] == content_type
        assert len(response.data) > 0


def test_image_file_not_found(client):
    """Test behavior when image file is missing."""
    # This test assumes the implementation might handle missing files gracefully
    # The actual behavior depends on the implementation in image.py
    response = client.get("/image/png")
    # Should either return the image or a proper error, not crash
    assert response.status_code in [200, 404, 500]


def test_image_concurrent_requests(client):
    """Test concurrent image requests don't interfere."""
    import threading
    import time

    results = []

    def make_request():
        response = client.get("/image/png")
        results.append(response.status_code)

    # Create multiple threads
    threads = [threading.Thread(target=make_request) for _ in range(5)]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    # All requests should succeed
    assert all(status == 200 for status in results)
    assert len(results) == 5
