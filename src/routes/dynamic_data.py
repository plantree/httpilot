"""Dynamic data routes."""

import uuid
from flask import Blueprint, json, request, jsonify, make_response, Response, url_for
import base64
import time
import random
from six.moves import range as xrange

from .http_methods import get_request_info

from .utils import utcnow

bp = Blueprint("dynamic_data", __name__)


@bp.route("/delay/<int:seconds>")
def delay_response(seconds):
    """Return a delayed response."""
    if seconds > 60:
        return jsonify({"error": "Maximum delay is 60 seconds"}), 400

    start_time = time.time()
    time.sleep(seconds)
    end_time = time.time()

    return jsonify(
        {
            "delay": seconds,
            "actual_delay": round(end_time - start_time, 3),
            "timestamp": utcnow(),
            "message": f"Delayed response after {seconds} seconds",
        }
    )


@bp.route("/base64/decoding/<value>")
def base64_decoding(value):
    """Encodes the given string to base64url-encoded."""
    encoded = value.encode("utf-8")  # base64 expects a binary string
    try:
        return base64.urlsafe_b64decode(encoded).decode("utf-8")
    except:
        return "Incorrect Base64 data try: aGVsbG93b3JsZA==", 400


@bp.route("/base64/encoding/<value>")
def base64_encoding(value):
    """Decodes base64url-encoded string."""
    encoded = value.encode("utf-8")
    return base64.urlsafe_b64encode(encoded).decode("utf-8")


@bp.route("/bytes/<int:n>")
def random_bytes(n):
    """Returns n random bytes generated with given seed."""
    n = min(n, 1000 * 1024)  # 100kb limited
    if "seed" in request.args.items():
        random.seed(int(request.args["seed"]))

    response = make_response()

    response.data = bytearray(random.randint(0, 255) for i in range(n))
    response.content_type = "application/octet-stream"
    return response


@bp.route("/uuid")
def view_uuid():
    """Return a UUID4."""
    response_data = {"uuid": uuid.uuid4(), "timestamp": utcnow()}

    return jsonify(response_data)


@bp.route("/stream/<int:n>")
def stream_n_messages(n):
    """Stream n JSON responses."""
    n = min(n, 100)
    response = get_request_info()

    def generate_stream():
        for i in range(n):
            response["id"] = i
            yield json.dumps(response) + "\n"

    return Response(generate_stream(), headers={"Content-Type": "application/json"})


@bp.route("/stream-bytes/<int:n>")
def stream_random_bytes(n):
    """Streams n random bytes generated with given seed, at given chunk suze per packet."""
    n = min(n, 100 * 1024)  # set 100kb limited
    if "seed" in request.args:
        random.seed(int(request.args["seed"]))

    if "chunk_size" in request.args:
        chunk_size = max(1, int(request.args["chunk_size"]))
    else:
        chunk_size = 10 * 1024

    def generate_bytes():
        chunks = bytearray()

        for i in xrange(n):
            chunks.append(random.randint(0, 255))
            if len(chunks) == chunk_size:
                yield (bytes(chunks))
                chunks = bytearray()

        if chunks:
            yield (bytes(chunks))

    return Response(
        generate_bytes(), headers={"Content-Type": "application/octet-stream"}
    )


@bp.route("/drip")
def drip():
    """Drips data over a duration after an optional initial delay."""
    args = request.args
    duration = float(args.get("duration", 2))
    numbytes = min(int(args.get("numbytes", 10)), 10 * 1024 * 1024)  # set 10mb limited
    code = int(args.get("code", 200))

    if numbytes <= 0:
        return Response("number of bytes must be positive", status=400)

    delay = float(args.get("delay", 0))
    if delay > 0:
        time.sleep(delay)

    pause = duration / numbytes

    def generate_byte():
        for i in xrange(numbytes):
            yield b"*"
            time.sleep(pause)

    return Response(
        generate_byte(),
        headers={
            "Content-Type": "application/octet-stream",
            "Content-Length": str(numbytes),
        },
        status=code,
    )


@bp.route("/links/<int:n>/<int:offset>")
def link_page(n, offset):
    """Generate a page containing n links to other pages which do the same."""
    n = min(max(1, n), 200)  # limit to between 1 and 200 links

    link = "<a href='{0}'>{1}</a> "
    html = ["<html><head><title>Links</title></head><body>"]

    for i in xrange(n):
        if i == offset:
            html.append("{0} ".format(i))
        else:
            html.append(
                link.format(url_for("dynamic_data.link_page", n=n, offset=i), i)
            )
    html.append("</body></html>")

    return "".join(html)


def __parse_request_range(range_header_text):
    """Return a tuple describing the byte range rquested in a GET request.
    If the range is open ended on the left or right side, then a value of None
    will be set.
    RFC7233: http://svn.tools.ietf.org/svn/wg/httpbis/specs/rfc7233.html#header.range
    Examples:
      Range : bytes=1024-
      Range : bytes=10-20
      Range : bytes=-999
    """
    left = None
    right = None

    if not range_header_text:
        return left, right

    components = range_header_text.split("=")
    if len(components) != 2:
        return left, right

    components = components[1].split("-")
    try:
        right = int(components[1])
    except:
        pass

    try:
        left = int(components[0])
    except:
        pass

    return left, right


def get_request_range(request_headers, upper_bound):
    first_byte_pos, last_byte_pos = __parse_request_range(
        request_headers.get("range", None)
    )

    if first_byte_pos is None and last_byte_pos is None:
        # Request full range
        first_byte_pos = 0
        last_byte_pos = upper_bound - 1
    elif first_byte_pos is None:
        # Request the last X bytes
        first_byte_pos = max(0, upper_bound - last_byte_pos)
        last_byte_pos = upper_bound - 1
    elif last_byte_pos is None:
        # Request the last X bytes
        last_byte_pos = upper_bound - 1

    return first_byte_pos, last_byte_pos


@bp.route("/range/<int:numbytes>")
def range_request(numbytes):
    """Streams n random bytes generated with given seed, at given chunk size per packet."""
    if numbytes <= 0 or numbytes > (100 * 1024):
        response = Response(
            headers={"ETag": f"range{numbytes}", "Accept-Ranges": "bytes"}
        )
        response.status_code = 400
        response.data = "number of bytes must be in the range (0, 102400)"
        return response

    params = request.args
    if "chunk_size" in params:
        chunk_size = max(1, int(params["chunk_size"]))
    else:
        chunk_size = 10 * 1024

    duration = float(params.get("duration", 0))
    pause_per_byte = duration / numbytes

    request_headers = request.headers
    first_byte_pos, last_byte_pos = get_request_range(request_headers, numbytes)
    range_length = last_byte_pos - first_byte_pos + 1

    if (
        first_byte_pos > last_byte_pos
        or first_byte_pos not in xrange(0, numbytes)
        or last_byte_pos not in xrange(0, numbytes)
    ):
        response = Response(
            headers={
                "ETag": f"range{numbytes}",
                "Accept_Ranges": "bytes",
                "Content-Range": f"bytes */{numbytes}",
                "Content-Length": "0",
            }
        )
        response.status_code = 416
        return response

    def generate_bytes():
        chunks = bytearray()

        for i in xrange(first_byte_pos, last_byte_pos + 1):
            # We don't want the resource to change across requests, so we need
            # to use a predictable data generation function.
            chunks.append(ord("a") + (i % 26))
            if len(chunks) == chunk_size:
                yield bytes(chunks)
                time.sleep(pause_per_byte * chunk_size)
                chunks = bytearray()

        if chunks:
            time.sleep(pause_per_byte * len(chunks))
            yield bytes(chunks)

    content_range = f"byte {first_byte_pos}-{last_byte_pos}/{numbytes}"
    response_headers = {
        "Content-Type": "application/octet-stream",
        "ETag": f"range{numbytes}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(range_length),
        "Content-Range": content_range,
    }

    response = Response(generate_bytes(), headers=response_headers)

    if first_byte_pos == 0 and last_byte_pos == numbytes - 1:
        response.status_code = 200
    else:
        response.status_code = 206

    return response
