"""
    This module contains the WTForm classes that handle the forms for bundling
    and unbundling (canceling) Certificates.
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
    owner_id = SelectField(
        label = "Initial owner",
        render_kw = { "placeholder" : "Select shareholder" }
    )



class CancellationForm(FlaskForm):
    id = StringField(render_kw = { "hidden" : True })
    shares = StringField(
        label = "Certificate",
        render_kw = { "readonly" : True }
    )
    last_transaction = DateField(
        label = "Date of last transaction",
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
                earlier = "last_transaction",
                message = "Cannot be earlier than date of last transaction"
            ),
            NotFutureDate()
        ]
    )
