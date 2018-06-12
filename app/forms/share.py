"""
    This module contains the WTForm class that handles the form for issuing new
    Shares. It uses the standard Flask-WTForm base class. Some custom validation
    is needed.
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
    MAX_SHARES = os.environ.get("MAX_SHARES")



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
        u = field.data
        l = form.lower_bound.data

        if type(u) != int:
            raise ValidationError()

        if u < l:
            raise ValidationError("Must be at least %s" % l)

        ## SAFEGUARD FOR PRODUCTION (DB IS VERY LIMITED)
        if MAX_SHARES and u > MAX_SHARES:
            raise ValidationError("Sorry but free trial supports only up to %s shares. GIVE ME MONEY") % MAX_SHARES
