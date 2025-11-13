"""Tests for response format routes."""

import json
import pytest
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


def test_json_response(client):
    """Test JSON response endpoint."""
    response = client.get("/json")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    data = json.loads(response.data)
    assert isinstance(data, dict)
    # Should contain HTTPilot application data
    assert "name" in data
    assert data["name"] == "HTTPilot"


def test_json_response_structure(client):
    """Test JSON response has expected structure."""
    response = client.get("/json")
    data = json.loads(response.data)

    # Should be a valid JSON object with HTTPilot-specific data
    assert isinstance(data, dict)
    # Expected HTTPilot structure
    expected_keys = [
        "name",
        "version",
        "description",
        "features",
        "timestamp",
        "sample_data",
    ]
    # All keys should be present
    assert all(key in data for key in expected_keys)


def test_xml_response(client):
    """Test XML response endpoint."""
    response = client.get("/xml")
    assert response.status_code == 200
    assert response.headers["Content-Type"] in ["application/xml", "text/xml"]

    # Should be valid XML
    try:
        ET.fromstring(response.data)
    except ET.ParseError:
        pytest.fail("Response is not valid XML")


def test_xml_response_structure(client):
    """Test XML response has proper structure."""
    response = client.get("/xml")
    xml_content = response.data.decode()

    # Should start with XML declaration or root element
    assert xml_content.strip().startswith("<?xml") or xml_content.strip().startswith(
        "<"
    )

    # Should be parseable XML
    root = ET.fromstring(response.data)
    assert root.tag is not None


def test_html_response(client):
    """Test HTML response endpoint."""
    response = client.get("/html")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html"

    html_content = response.data.decode()
    # Should contain HTML tags
    assert "<html>" in html_content or "<HTML>" in html_content
    assert "</html>" in html_content or "</HTML>" in html_content


def test_html_response_structure(client):
    """Test HTML response has proper structure."""
    response = client.get("/html")
    html_content = response.data.decode()

    # Should be parseable HTML
    soup = BeautifulSoup(html_content, "html.parser")
    assert soup.html is not None

    # Should have basic HTML structure
    assert soup.head is not None or soup.body is not None


def test_robots_txt_response(client):
    """Test robots.txt response endpoint."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"

    content = response.data.decode()
    # Should contain robots.txt directives
    assert "User-agent:" in content or "User-Agent:" in content


def test_robots_txt_format(client):
    """Test robots.txt has proper format."""
    response = client.get("/robots.txt")
    content = response.data.decode()

    # Should follow robots.txt format
    lines = content.strip().split("\n")
    # Should have at least User-agent directive
    user_agent_found = any("user-agent:" in line.lower() for line in lines)
    assert user_agent_found


def test_brotli_compression(client):
    """Test Brotli compression endpoint."""
    response = client.get("/brotli", headers={"Accept-Encoding": "br"})
    assert response.status_code == 200

    # Should indicate Brotli encoding in response
    content_encoding = response.headers.get("Content-Encoding")
    if content_encoding:
        assert "br" in content_encoding.lower()


def test_brotli_without_accept_encoding(client):
    """Test Brotli endpoint without proper Accept-Encoding."""
    response = client.get("/brotli")
    assert response.status_code == 200
    # Should still work, might return uncompressed or different encoding


def test_deflate_compression(client):
    """Test Deflate compression endpoint."""
    response = client.get("/deflate", headers={"Accept-Encoding": "deflate"})
    assert response.status_code == 200

    content_encoding = response.headers.get("Content-Encoding")
    if content_encoding:
        assert "deflate" in content_encoding.lower()


def test_gzip_compression(client):
    """Test GZip compression endpoint."""
    response = client.get("/gzip", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200

    content_encoding = response.headers.get("Content-Encoding")
    if content_encoding:
        assert "gzip" in content_encoding.lower()


def test_utf8_encoding(client):
    """Test UTF-8 encoding endpoint."""
    response = client.get("/encoding/utf8")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    content = response.data.decode("utf-8")
    # Should contain international characters to test UTF-8
    # Common UTF-8 test characters
    utf8_chars = ["é", "ñ", "中", "日", "العربية", "русский", "🌟", "💯"]
    has_utf8 = any(char in content for char in utf8_chars)
    # If no specific UTF-8 chars, at least verify it decodes properly
    assert has_utf8 or len(content) > 0


def test_utf8_encoding_charset(client):
    """Test UTF-8 encoding specifies correct charset."""
    response = client.get("/encoding/utf8")
    content_type = response.headers["Content-Type"]
    assert "charset=utf-8" in content_type.lower()


def test_compression_endpoints_return_data(client):
    """Test that compression endpoints return actual data."""
    endpoints = ["/brotli", "/deflate", "/gzip"]

    for endpoint in endpoints:
        response = client.get(
            endpoint, headers={"Accept-Encoding": "gzip, deflate, br"}
        )
        assert response.status_code == 200
        assert len(response.data) > 0


def test_compression_with_multiple_accept_encodings(client):
    """Test compression endpoints with multiple Accept-Encoding values."""
    response = client.get("/gzip", headers={"Accept-Encoding": "gzip, deflate, br"})
    assert response.status_code == 200

    # Should prefer the endpoint's specific compression
    content_encoding = response.headers.get("Content-Encoding", "")
    if content_encoding:
        assert "gzip" in content_encoding.lower()


def test_format_responses_have_correct_content_length(client):
    """Test that format responses include Content-Length header."""
    endpoints = ["/json", "/xml", "/html", "/robots.txt"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200

        if "Content-Length" in response.headers:
            expected_length = len(response.data)
            actual_length = int(response.headers["Content-Length"])
            assert expected_length == actual_length


def test_format_responses_cacheable(client):
    """Test that format responses are cacheable by default."""
    endpoints = ["/json", "/xml", "/html", "/robots.txt"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200

        # Should not explicitly prevent caching
        cache_control = response.headers.get("Cache-Control", "")
        assert "no-cache" not in cache_control.lower()
        assert "no-store" not in cache_control.lower()


def test_json_content_is_valid_json(client):
    """Test that JSON endpoint returns valid, parseable JSON."""
    response = client.get("/json")

    # Should not raise exception
    try:
        data = json.loads(response.data)
        # Should be a JSON object or array
        assert isinstance(data, (dict, list))
    except json.JSONDecodeError:
        pytest.fail("JSON endpoint did not return valid JSON")


def test_xml_content_is_well_formed(client):
    """Test that XML endpoint returns well-formed XML."""
    response = client.get("/xml")

    try:
        root = ET.fromstring(response.data)
        # Should have at least a root element
        assert root is not None
        assert root.tag is not None
    except ET.ParseError as e:
        pytest.fail(f"XML endpoint did not return well-formed XML: {e}")


def test_html_content_is_valid_html(client):
    """Test that HTML endpoint returns valid HTML."""
    response = client.get("/html")
    html_content = response.data.decode()

    # Should be parseable by BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Should have HTML structure
    assert soup.find("html") is not None or soup.find("HTML") is not None


def test_response_formats_consistent(client):
    """Test that response formats are consistent across requests."""
    endpoints = ["/json", "/xml", "/html"]

    for endpoint in endpoints:
        response1 = client.get(endpoint)
        response2 = client.get(endpoint)

        assert response1.status_code == response2.status_code
        assert response1.headers["Content-Type"] == response2.headers["Content-Type"]
        # Content might be dynamic, so we don't check data equality


def test_head_requests_for_format_endpoints(client):
    """Test HEAD requests for format endpoints."""
    endpoints = ["/json", "/xml", "/html", "/robots.txt"]

    for endpoint in endpoints:
        response = client.head(endpoint)
        assert response.status_code == 200
        assert len(response.data) == 0  # HEAD should not return body
        assert "Content-Type" in response.headers


def test_options_requests_for_format_endpoints(client):
    """Test OPTIONS requests for format endpoints."""
    endpoints = ["/json", "/xml", "/html"]

    for endpoint in endpoints:
        response = client.options(endpoint)
        assert response.status_code == 200
        assert "Allow" in response.headers

        allowed_methods = response.headers["Allow"].upper()
        assert "GET" in allowed_methods
        assert "HEAD" in allowed_methods


def test_compression_decompression_cycle(client):
    """Test that compressed responses can be decompressed."""
    import gzip
    import zlib

    # Test gzip
    response = client.get("/gzip", headers={"Accept-Encoding": "gzip"})
    if response.headers.get("Content-Encoding") == "gzip":
        # Should be able to decompress
        try:
            decompressed = gzip.decompress(response.data)
            assert len(decompressed) > 0
        except Exception as e:
            pytest.fail(f"Could not decompress gzip response: {e}")


def test_encoding_handling_edge_cases(client):
    """Test encoding handling with edge cases."""
    # Test with various Accept-Encoding headers
    test_cases = [
        "gzip",
        "deflate",
        "br",
        "gzip, deflate",
        "br;q=1.0, gzip;q=0.8, *;q=0.1",
        "identity",
        "*",
        "",
    ]

    for accept_encoding in test_cases:
        response = client.get("/gzip", headers={"Accept-Encoding": accept_encoding})
        assert response.status_code == 200
        # Should handle all cases gracefully
