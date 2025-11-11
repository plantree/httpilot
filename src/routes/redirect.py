"""Returns different redirect responses."""

from flask import Blueprint, request, url_for, redirect, make_response, jsonify

from .utils import utcnow

bp = Blueprint("redirect", __name__)


@bp.route("/redirect/<int:n>")
def redirect_times(n):
    """302 Redirects n times."""
    assert n > 0

    absolute = request.args.get("absolute", "false").lower() == "true"

    if n == 1:
        return redirect(url_for("http_methods.view_get", _external=absolute))

    if absolute:
        return _redirect("absolute", n, True)
    else:
        return _redirect("relative", n, False)


def _redirect(kind, n, external):
    return redirect(
        url_for(f"redirect.{kind}_redirect_n_times", n=n - 1, _external=external)
    )


@bp.route("/absolute-redirect/<int:n>")
def absolute_redirect_n_times(n):
    """Absolutely 302 Redirects n times."""
    assert n > 0

    if n == 1:
        return redirect(url_for("http_methods.view_get", _external=True))
    return _redirect("absolute", n, True)


@bp.route("/relative-redirect/<int:n>")
def relative_redirect_n_times(n):
    """Relatively 302 Redirects n times."""
    assert n > 0

    response = make_response()
    response.status_code = 302

    if n == 1:
        return redirect(url_for("http_methods.view_get", _external=False))

    return _redirect("relative", n, False)


def is_int(str):
    try:
        n = int(str)
        return True
    except:
        return False


@bp.route("/redirect-to", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
def redirect_to():
    """302/3XX redirects to the given URL."""
    args = request.args

    if (
        "status_code" not in args
        or not is_int(args["status_code"])
        or "url" not in args
    ):
        response = jsonify(
            {
                "message": "invalid input. Example: /redirect-to?url=ip&status_code=302",
                "timestamp": utcnow(),
            }
        )
        response.status_code = 400
        return response

    response = make_response()
    response.status_code = 302
    status_code = int(args["status_code"])
    if status_code >= 300 and status_code < 400:
        response.status_code = status_code
    response.headers["Location"] = args["url"]

    return response
