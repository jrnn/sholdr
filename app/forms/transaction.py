"""
    This module contains the WTForm class that handles the forms for recording
    Transactions. A tweaked base class that trims surrounding whitespace from
    all fields is applied.
"""

from . import CustomBaseForm
from .validators import (
    MaxLength,
    NotFutureDate
)
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DecimalField,
    SelectField,
    StringField,
    TextAreaField,
    validators
)



class TransactionForm(CustomBaseForm):
    certificate_id = StringField(render_kw = { "hidden" : True })
    shares = StringField(
        label = "Certificate",
        render_kw = { "readonly" : True }
    )
    owner = StringField(
        label = "Current owner",
        render_kw = { "readonly" : True }
    )
    shareholder_id = SelectField(
        label = "New owner",
        render_kw = { "placeholder" : "Select shareholder" }
        # cannot be empty
        # cannot be same as current owner
    )
    recorded_on = DateField(
        label = "Transaction date",
        render_kw = {
            "placeholder" : "Pick a date",
            "type" : "date"
        },
        validators = [ NotFutureDate() ]
        # cannot precede earlier transactions
    )
    price = DecimalField(
        default = 0,
        label = "Price (EUR)",
        render_kw = { "placeholder" : "Use '.' as decimal point" },
        validators = [
            validators.NumberRange(
                message = "Must be positive number",
                min = 0
            )
        ]
    )
    remarks = TextAreaField(
        label = "Remarks",
        validators = [ MaxLength(255) ]
    )
