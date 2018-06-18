"""
    This module contains the WTForm class that handles the login form.
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
        filters = [
            apply_lower,
            apply_strip
        ],
        label = "Email",
        render_kw = { "placeholder" : "fred@flintstone.io" }
    )
    password = PasswordField(
        label = "Password",
        render_kw = { "placeholder" : "qwerty" }
    )
