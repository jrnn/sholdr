"""
    This module contains the WTForm class that handles the Share Class form.
"""

from . import CustomBaseForm
from .validators import (
    MaxLength,
    NotEmpty,
    Unique
)
from wtforms import (
    IntegerField,
    StringField,
    TextAreaField,
    validators
)



class ShareClassForm(CustomBaseForm):
    id = StringField(
        default = "new",
        render_kw = { "hidden" : True }
    )
    name = StringField(
        label = "Class name",
        render_kw = { "placeholder" : "e.g. A, B, C ..." },
        validators = [
            MaxLength(32),
            NotEmpty(),
            Unique(
                column = "name",
                message = "Class name must be unique",
                table = "share_class"
            )
        ]
    )
    votes = IntegerField(
        default = 1,
        label = "Votes per share",
        render_kw = { "placeholder" : "Give an integer" },
        validators = [
            validators.NumberRange(
                message = "Must be non-negative integer",
                min = 0
            )
        ]
    )
    remarks = TextAreaField(
        label = "Remarks",
        render_kw = { "placeholder" : "E.g. description of ownership rules or privileges other than number of votes" },
        validators = [ MaxLength(255) ]
    )
