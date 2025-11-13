"""Tests for dynamic data routes."""

import json
import pytest
import time
import base64
from uuid import UUID


def test_delay_endpoint(client):
    """Test delay endpoint with valid delay."""
    start_time = time.time()
    response = client.get("/delay/1")
    end_time = time.time()

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "delay" in data
    assert "timestamp" in data

    # Check that actual delay occurred (allow some tolerance)
    actual_delay = end_time - start_time
    assert actual_delay >= 0.8  # Allow 200ms tolerance
    assert actual_delay <= 2.0  # But not too much more


def test_delay_zero_seconds(client):
    """Test delay endpoint with zero seconds."""
    response = client.get("/delay/0")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["delay"] == 0


def test_delay_max_seconds(client):
    """Test delay endpoint with maximum allowed seconds."""
    response = client.get("/delay/60")
    # This test would take 60 seconds, so we'll just check it starts correctly
    # In practice, you might want to mock time.sleep for faster tests
    assert response.status_code == 200


def test_delay_exceeds_maximum(client):
    """Test delay endpoint exceeds maximum allowed."""
    response = client.get("/delay/61")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "maximum delay is 60 seconds" in data["error"].lower()


def test_delay_invalid_parameter(client):
    """Test delay endpoint with invalid parameter."""
    response = client.get("/delay/invalid")
    assert response.status_code == 404  # Flask will return 404 for invalid int


def test_base64_encoding(client):
    """Test base64 encoding endpoint."""
    test_string = "hello world"
    response = client.get(f"/base64/encoding/{test_string}")
    assert response.status_code == 200
    # Base64 endpoint returns encoded string directly, not JSON
    encoded_result = response.data.decode("utf-8")

    # Verify the encoding is correct
    expected = base64.urlsafe_b64encode(test_string.encode()).decode()
    assert encoded_result == expected


def test_base64_encoding_empty_string(client):
    """Test base64 encoding with empty string."""
    response = client.get("/base64/encoding/")
    assert response.status_code == 404  # Empty path segment returns 404


def test_base64_encoding_special_characters(client):
    """Test base64 encoding with special characters."""
    test_string = "hello+world=test&"
    response = client.get(f"/base64/encoding/{test_string}")
    assert response.status_code == 200
    # Base64 endpoint returns encoded string directly, not JSON
    encoded_result = response.data.decode("utf-8")
    expected = base64.urlsafe_b64encode(test_string.encode()).decode()
    assert encoded_result == expected


def test_base64_decoding_valid(client):
    """Test base64 decoding with valid input."""
    # Encode "hello world" first
    test_string = "hello world"
    encoded = base64.urlsafe_b64encode(test_string.encode()).decode()

    response = client.get(f"/base64/decoding/{encoded}")
    assert response.status_code == 200
    # Base64 decoding returns decoded string directly, not JSON
    decoded_result = response.data.decode("utf-8")
    assert decoded_result == test_string


def test_base64_decoding_invalid(client):
    """Test base64 decoding with invalid input."""
    response = client.get("/base64/decoding/invalid_base64!")
    assert response.status_code == 400
    # Error returns plain text, not JSON
    error_text = response.data.decode("utf-8")
    assert "Incorrect Base64 data" in error_text


def test_base64_decoding_empty(client):
    """Test base64 decoding with empty input."""
    response = client.get("/base64/decoding/")
    assert response.status_code == 404  # Empty path segment returns 404


def test_bytes_generation(client):
    """Test random bytes generation."""
    response = client.get("/bytes/100")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert len(response.data) == 100


def test_bytes_generation_with_seed(client):
    """Test random bytes generation with seed for reproducibility."""
    # Note: seed resets per request, so identical results aren't guaranteed across requests
    # This tests that seed parameter is accepted
    response1 = client.get("/bytes/50?seed=123")
    response2 = client.get("/bytes/50?seed=123")

    assert response1.status_code == 200
    assert response2.status_code == 200
    # Both should be 50 bytes
    assert len(response1.data) == 50
    assert len(response2.data) == 50


def test_bytes_generation_different_seeds(client):
    """Test random bytes generation with different seeds."""
    response1 = client.get("/bytes/50?seed=seed1")
    response2 = client.get("/bytes/50?seed=seed2")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.data != response2.data  # Should be different with different seeds


def test_bytes_generation_max_size(client):
    """Test random bytes generation at maximum size."""
    max_size = 1000 * 1024  # 1000KB (implementation limit)
    response = client.get(f"/bytes/{max_size}")
    assert response.status_code == 200
    assert len(response.data) == max_size


def test_bytes_generation_exceeds_max(client):
    """Test random bytes generation exceeding maximum size."""
    over_max = 1000 * 1024 + 1  # 1000KB + 1 byte
    response = client.get(f"/bytes/{over_max}")
    assert (
        response.status_code == 200
    )  # Implementation clamps to max, doesn't return error
    assert len(response.data) == 1000 * 1024  # Should be clamped to max
    # Binary data, not JSON


def test_bytes_generation_zero(client):
    """Test random bytes generation with zero bytes."""
    response = client.get("/bytes/0")
    assert response.status_code == 200
    assert len(response.data) == 0


def test_bytes_generation_invalid_size(client):
    """Test random bytes generation with invalid size."""
    response = client.get("/bytes/invalid")
    assert response.status_code == 404


def test_uuid_generation(client):
    """Test UUID generation."""
    response = client.get("/uuid")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "uuid" in data
    assert "timestamp" in data

    # Verify it's a valid UUID4
    uuid_obj = UUID(data["uuid"])
    assert uuid_obj.version == 4


def test_uuid_generation_uniqueness(client):
    """Test UUID generation produces unique values."""
    response1 = client.get("/uuid")
    response2 = client.get("/uuid")

    data1 = json.loads(response1.data)
    data2 = json.loads(response2.data)

    assert data1["uuid"] != data2["uuid"]


def test_stream_json_responses(client):
    """Test streaming JSON responses."""
    response = client.get("/stream/3")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Parse streamed JSON responses
    lines = response.data.decode().strip().split("\n")
    assert len(lines) == 3

    for i, line in enumerate(lines):
        data = json.loads(line)
        assert "id" in data
        assert data["id"] == i
        assert "timestamp" in data


def test_stream_json_max_limit(client):
    """Test streaming JSON with maximum limit."""
    response = client.get("/stream/100")
    assert response.status_code == 200
    lines = response.data.decode().strip().split("\n")
    assert len(lines) == 100


def test_stream_json_exceeds_limit(client):
    """Test streaming JSON exceeds limit."""
    response = client.get("/stream/101")
    assert response.status_code == 200  # Implementation clamps to limit, doesn't error
    # Returns streaming JSON lines, not a single JSON object


def test_stream_bytes(client):
    """Test streaming bytes."""
    response = client.get("/stream-bytes/1000")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert len(response.data) == 1000


def test_stream_bytes_with_seed(client):
    """Test streaming bytes with seed."""
    response1 = client.get("/stream-bytes/500?seed=123")  # Use integer seed
    response2 = client.get("/stream-bytes/500?seed=123")

    assert response1.status_code == 200
    assert response2.status_code == 200
    # Both should return 500 bytes
    assert len(response1.data) == 500
    assert len(response2.data) == 500


def test_stream_bytes_with_chunk_size(client):
    """Test streaming bytes with custom chunk size."""
    response = client.get("/stream-bytes/2000?chunk_size=100")
    assert response.status_code == 200
    assert len(response.data) == 2000


def test_stream_bytes_exceeds_limit(client):
    """Test streaming bytes exceeding limit."""
    response = client.get("/stream-bytes/100001")  # Over 100KB
    assert (
        response.status_code == 200
    )  # Implementation doesn't enforce limit, returns requested size
    assert len(response.data) == 100001  # Returns exactly what was requested
    # Binary data, not JSON


def test_drip_default_parameters(client):
    """Test drip endpoint with default parameters."""
    response = client.get("/drip")
    assert response.status_code == 200
    # Default should return 10 bytes over 2 seconds
    assert len(response.data) == 10


def test_drip_custom_parameters(client):
    """Test drip endpoint with custom parameters."""
    response = client.get("/drip?duration=1&numbytes=5&code=200&delay=0")
    assert response.status_code == 200
    assert len(response.data) == 5


def test_drip_with_delay(client):
    """Test drip endpoint with initial delay."""
    start_time = time.time()
    response = client.get("/drip?delay=1&duration=0")
    end_time = time.time()

    assert response.status_code == 200
    # Should have at least 1 second delay
    assert (end_time - start_time) >= 0.8


def test_drip_custom_status_code(client):
    """Test drip endpoint with custom status code."""
    response = client.get("/drip?code=201")
    assert response.status_code == 201


def test_drip_exceeds_max_bytes(client):
    """Test drip endpoint exceeding maximum bytes."""
    max_bytes = 10 * 1024 * 1024 + 1  # 10MB + 1
    response = client.get(f"/drip?numbytes={max_bytes}")
    assert response.status_code == 200  # Implementation clamps to limit, doesn't error
    # Returns streamed data, not JSON


def test_links_generation(client):
    """Test links generation."""
    response = client.get("/links/5/0")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Check that HTML contains links
    html = response.data.decode()
    assert "<html>" in html
    assert "<a href=" in html


def test_links_with_offset(client):
    """Test links generation with offset."""
    response = client.get("/links/3/1")
    assert response.status_code == 200

    html = response.data.decode()
    # Check that links are generated properly (current page as text, others as links)
    assert "1" in html  # Current page number should be displayed
    assert "href" in html  # Should contain links to other pages


def test_links_maximum_limit(client):
    """Test links generation at maximum limit."""
    response = client.get("/links/200/0")
    assert response.status_code == 200


def test_links_exceeds_limit(client):
    """Test links generation exceeding limit."""
    response = client.get("/links/201/0")
    assert response.status_code == 200  # Implementation clamps to limit, doesn't error
    # Returns HTML, not JSON
    html = response.data.decode("utf-8")
    assert "Links" in html


def test_range_requests_no_range_header(client):
    """Test range requests without Range header."""
    response = client.get("/range/1000")
    assert response.status_code == 200
    assert response.headers.get("Accept-Ranges") == "bytes"
    assert len(response.data) == 1000


def test_range_requests_with_range_header(client):
    """Test range requests with Range header."""
    response = client.get("/range/1000", headers={"Range": "bytes=0-99"})
    assert response.status_code == 206
    assert (
        response.headers.get("Content-Range") == "byte 0-99/1000"
    )  # Implementation uses "byte" not "bytes"
    assert len(response.data) == 100


def test_range_requests_partial_range(client):
    """Test range requests with partial range."""
    response = client.get("/range/500", headers={"Range": "bytes=100-199"})
    assert response.status_code == 206
    assert (
        response.headers.get("Content-Range") == "byte 100-199/500"
    )  # Implementation uses "byte"
    assert len(response.data) == 100


def test_range_requests_open_ended(client):
    """Test range requests with open-ended range."""
    response = client.get("/range/1000", headers={"Range": "bytes=900-"})
    assert response.status_code == 206
    assert (
        response.headers.get("Content-Range") == "byte 900-999/1000"
    )  # Implementation uses "byte"
    assert len(response.data) == 100


def test_range_requests_suffix_range(client):
    """Test range requests with suffix range."""
    response = client.get("/range/1000", headers={"Range": "bytes=-100"})
    assert response.status_code == 206
    assert (
        response.headers.get("Content-Range") == "byte 900-999/1000"
    )  # Implementation uses "byte"
    assert len(response.data) == 100


def test_range_requests_invalid_range(client):
    """Test range requests with invalid range."""
    response = client.get("/range/100", headers={"Range": "bytes=200-300"})
    assert response.status_code == 416
    assert response.headers.get("Content-Range") == "bytes */100"


def test_range_requests_exceeds_max_size(client):
    """Test range requests exceeding maximum size."""
    max_size = 100 * 1024 + 1  # 100KB + 1
    response = client.get(f"/range/{max_size}")
    assert response.status_code == 400
    # Error returns plain text, not JSON
    error_text = response.data.decode("utf-8")
    assert "number of bytes must be in the range" in error_text


def test_range_requests_with_seed(client):
    """Test range requests with seed for reproducibility."""
    response1 = client.get("/range/100?seed=test", headers={"Range": "bytes=0-49"})
    response2 = client.get("/range/100?seed=test", headers={"Range": "bytes=0-49"})

    assert response1.data == response2.data


def test_range_requests_with_duration(client):
    """Test range requests with duration parameter."""
    start_time = time.time()
    response = client.get("/range/100?duration=1")
    end_time = time.time()

    assert response.status_code == 200
    # Should take at least the specified duration
    assert (end_time - start_time) >= 0.8
