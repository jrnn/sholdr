"""
    This module contains the WTForm classes that handle the forms for bundling
    and unbundling (canceling) Certificates. Standard Flask-WTForm base class is
    used, and there is nothing special apart from a little custom validation.
"""

from .validators import (
    NotEarlierThan,
    NotFutureDate,
    PossibleBundleDate,
    WithinBounds
)
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    StringField
)



class CertificateForm(FlaskForm):
    first_share = IntegerField(
        label = "Starting from number ...",
        render_kw = { "placeholder" : "Give a positive integer" }
    )
    last_share = IntegerField(
        label = "... up to number",
        render_kw = { "placeholder" : "Give a positive integer" },
        validators = [ WithinBounds() ]
    )
    issued_on = DateField(
        label = "Issued on",
        render_kw = {
            "placeholder" : "Pick a date",
            "type" : "date"
        },
        validators = [
            NotFutureDate(),
            PossibleBundleDate()
        ]
    )
    shareholder_id = SelectField(
        choices = [ ("tba", "Not yet implemented") ],
        label = "Initial owner",
        render_kw = {
            "placeholder" : "Select shareholder",
            "readonly" : True
        }
    )



class CancellationForm(FlaskForm):
    id = StringField(render_kw = { "hidden" : True })
    shares = StringField(
        label = "Certificate",
        render_kw = { "readonly" : True }
    )
    issued_on = DateField(
        label = "Date of issue",
        render_kw = { "readonly" : True }
    )
    canceled_on = DateField(
        label = "Date of cancellation",
        render_kw = {
            "placeholder" : "Pick a date",
            "type" : "date"
        },
        validators = [
            NotEarlierThan(
                earlier = "issued_on",
                message = "Cannot be earlier than date of issue"
            ),
            NotFutureDate()
        ]
    )
