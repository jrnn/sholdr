"""
    This module contains the WTForm class that handles the forms for recording
    Transactions (i.e. transfers of certificate ownership).
"""

from . import CustomBaseForm
from .validators import (
    MaxLength,
    NotEarlierThan,
    NotEqualTo,
    NotFutureDate
)
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
    seller_id = StringField(render_kw = { "hidden" : True })
    last_transaction = DateField(
        label = "Date of last transaction",
        render_kw = { "readonly" : True }
    )
    shares = StringField(
        label = "Certificate",
        render_kw = { "readonly" : True }
    )
    seller = StringField(
        label = "Current owner",
        render_kw = { "readonly" : True }
    )
    buyer_id = SelectField(
        label = "New owner",
        render_kw = { "placeholder" : "Select shareholder" },
        validators = [
            NotEqualTo(
                message = "Cannot be same as current owner",
                other = "seller_id"
            )
        ]
    )
    recorded_on = DateField(
        label = "Transaction date",
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
