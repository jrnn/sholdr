"""
    This module contains the blueprint for user session management endpoints,
    i.e. login and logout operations.
"""

from app.config.auth import logout_user_memoized
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
    login_user
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
    logout_user_memoized()
    flash.logout_ok()
    return redirect(url_for("index"))
