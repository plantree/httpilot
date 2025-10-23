"""Returns different redirect responses."""

from flask import Blueprint, request, url_for, redirect, make_response

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
