"""
    This module contains the WTForm class that handles the form for issuing new
    Shares.
"""

import os

from .validators import (
    NotEarlierThan,
    NotFutureDate
)
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    ValidationError
)

MAX_SHARES = None
if os.environ.get("HEROKU"):
    MAX_SHARES = int(os.environ.get("MAX_SHARES"))



class ShareForm(FlaskForm):
    lower_bound = IntegerField(
        label = "Starting from number ...",
        render_kw = { "readonly" : True }
    )
    upper_bound = IntegerField(
        label = "... up to number",
        render_kw = { "placeholder" : "Give a positive integer" }
    )
    latest_issue = DateField(
        label = "Latest issue date",
        render_kw = { "readonly" : True }
    )
    issued_on = DateField(
        label = "Issued on",
        render_kw = {
            "placeholder" : "Pick a date",
            "type" : "date"
        },
        validators = [
            NotEarlierThan(
                earlier = "latest_issue",
                message = "Cannot be earlier than date of the latest issue"
            ),
            NotFutureDate()
        ]
    )
    share_class_id = SelectField(
        label = "Share class",
        render_kw = { "placeholder" : "Select share class" }
    )

    def validate_upper_bound(form, field):
        upper = field.data
        lower = form.lower_bound.data

        if type(upper) != int:
            raise ValidationError()

        if upper < lower:
            raise ValidationError("Must be at least %s" % lower)

        ## SAFEGUARD FOR PRODUCTION (DB IS VERY LIMITED)
        if MAX_SHARES and upper > MAX_SHARES:
            raise ValidationError("Sorry but free trial supports only up to %s shares. GIVE ME MONEY") % MAX_SHARES
