"""
Provides response filter decorators.
"""
import brotli as _brotli
import gzip as _gzip
import zlib
from six import BytesIO
from flask import Response

from decorator import decorator


@decorator
def brotli(f, *args, **kwargs):
    """Brotli Flask response Decorator."""

    data = f(*args, **kwargs)

    if isinstance(data, Response):
        content = data.data
    else:
        content = data

    deflated_data = _brotli.compress(content)

    if isinstance(data, Response):
        data.data = deflated_data
        data.headers["Content-Encoding"] = "br"
        data.headers["Content-Length"] = str(len(data.data))

        return data
    return deflated_data


@decorator
def deflate(f, *args, **kwargs):
    """Deflate Flask Response Decorator."""

    data = f(*args, **kwargs)

    if isinstance(data, Response):
        content = data.data
    else:
        content = data

    deflater = zlib.compressobj()
    deflated_data = deflater.compress(content)
    deflated_data += deflater.flush()

    if isinstance(data, Response):
        data.data = deflated_data
        data.headers["Content-Encoding"] = "deflate"
        data.headers["Content-Length"] = str(len(data.data))

        return data

    return deflated_data


@decorator
def gzip(f, *args, **kwargs):
    """GZip Flask Response Decorator."""

    data = f(*args, **kwargs)

    if isinstance(data, Response):
        content = data.data
    else:
        content = data

    gzip_buffer = BytesIO()
    gzip_file = _gzip.GzipFile(mode="wb", compresslevel=4, fileobj=gzip_buffer)
    gzip_file.write(content)
    gzip_file.close()

    gzip_data = gzip_buffer.getvalue()

    if isinstance(data, Response):
        data.data = gzip_data
        data.headers["Content-Encoding"] = "gzip"
        data.headers["Content-Length"] = str(len(data.data))

        return data

    return gzip_data
