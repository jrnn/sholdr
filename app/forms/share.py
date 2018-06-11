"""
    This module contains the WTForm class that handles the form for issuing new
    Shares. It uses the standard Flask-WTForm base class. Some custom validation
    is needed.
"""

from .validators import NotFutureDate
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    ValidationError
)



class ShareForm(FlaskForm):
    lower_bound = IntegerField(
        label = "Starting from number ...",
        render_kw = { "readonly" : True }
    )
    upper_bound = IntegerField(
        label = "... up to number",
        render_kw = { "placeholder" : "Give a positive integer" }
    )
    issued_on = DateField(
        label = "Issued on",
        render_kw = {
            "placeholder" : "Pick a date",
            "type" : "date"
        },
        validators = [ NotFutureDate() ]
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

        ## TEMPORARY SAFEGUARD FOR PRODUCTION (DB IS VERY LIMITED)
        if u > 250:
            raise ValidationError("Sorry but free trial supports only up to 250 shares. GIVE ME MONEY")
