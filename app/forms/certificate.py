"""
    This module contains the WTForm class that handles the Certificate form. It
    uses the standard Flask-WTForm base class. Some custom validation is
    required.
"""

from app.util.validation import (
    NotFutureDate,
    WithinBounds
)
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField
)

class CertificateForm(FlaskForm):
    first_share = IntegerField(
        label = "Starting from number ...",
        render_kw = {"placeholder" : "Give a positive integer" }
    )
    last_share = IntegerField(
        label = "... up to number",
        render_kw = {"placeholder" : "Give a positive integer" },
        validators = [ WithinBounds() ]
    )
    issued_on = DateField(
        label = "Issued on",
        render_kw = {
            "placeholder" : "Pick a date",
            "type" : "date"
        },
        validators = [ NotFutureDate() ]
    )
    shareholder_id = SelectField(
        choices = [ ("tba", "Not yet implemented") ],
        label = "Initial owner",
        render_kw = {
            "placeholder" : "Select shareholder",
            "readonly" : True
        }
    )

    class Meta:
        csrf = False
