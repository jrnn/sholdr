"""
    This module contains the WTForm class that handles the login form. It uses
    the standard Flask-WTForm base class, and is altogether very simple with
    no validation or other intricacies.
"""

from app.util.util import (
    apply_lower,
    apply_strip
)
from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField
)

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        filters = [
            apply_lower,
            apply_strip
        ],
        render_kw = { "placeholder" : "fred@flintstone.io" }
    )
    password = PasswordField(
        "Password",
        render_kw = { "placeholder" : "qwerty" }
    )

    class Meta:
        csrf = False
