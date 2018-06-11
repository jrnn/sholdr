"""
    This module contains the blueprint for user session management endpoints,
    i.e. login and logout operations.
"""

from app.forms.auth import LoginForm
from app.models.shareholder import Shareholder
from app.util import notify
from app.util.auth import (
    checkPassword,
    logout_user_memoized
)
from flask import (
    Blueprint,
    redirect,
    render_template,
    request
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
        notify.login_error()
        return render_template(
            "auth/login.html",
            errors = [ "Invalid credentials" ],
            form = f
        )

    login_user(s)
    notify.login_ok()
    return redirect("/")



@bp.route("/logout")
@login_required
def logout():
    logout_user_memoized()
    notify.logout_ok()
    return redirect("/")
