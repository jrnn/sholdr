"""
    This module contains the blueprint for user session management endpoints,
    i.e. login and logout operations.

    TO-DO : Figure out how to remove only session-related cache key on logout.
"""

from app import cache
from app.forms.auth import LoginForm
from app.models.shareholder import Shareholder
from app.util import flash
from app.util.auth import checkPassword
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import (
    login_required,
    login_user,
    logout_user
)

bp = Blueprint(
    "auth",
    __name__
)

@bp.route("/login", methods = ("GET", "POST",))
def login():
    """
    Depending on request type, either (1) show login form, or (2) check that
    provided credentials are valid, and store authenticated user in the session.
    """
    if request.method == "GET":
        return render_template(
            "auth/login.html",
            form = LoginForm()
        )

    f = LoginForm(request.form)
    s = Shareholder.query.filter_by(email = f.email.data).first()

    if not s or not checkPassword(f.password.data, s.pw_hash) or not s.has_access:
        flash.login_error()
        return render_template(
            "auth/login.html",
            error = "Invalid credentials",
            form = f
        )

    login_user(s)
    flash.login_ok()
    return redirect(url_for("index"))

@bp.route("/logout")
@login_required
def logout():
    cache.clear() # need to clear whole cache because can't import the load_user function from inside init_auth ...
    logout_user()
    flash.logout_ok()
    return redirect(url_for("index"))
