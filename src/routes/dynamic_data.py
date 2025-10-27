"""Dynamic data routes."""

import uuid
from flask import Blueprint, json, request, jsonify, make_response, Response
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
