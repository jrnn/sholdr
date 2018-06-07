"""
    This module contains the WTForm class that handles the Share Class form. A
    tweaked base class that trims surrounding whitespace from all fields is
    applied. Some custom validation is needed.
"""

from . import CustomBaseForm
from app.models.shareclass import ShareClass
from app.util.validation import (
    max_length,
    not_empty,
    Unique
)
from wtforms import (
    IntegerField,
    StringField,
    TextAreaField,
    validators
)

class ShareClassForm(CustomBaseForm):
    id = StringField(default = "new")

    name = StringField(
        label = "Class name",
        render_kw = { "placeholder" : "e.g. A, B, C ..." },
        validators = [
            max_length(32),
            not_empty(),
            Unique(
                column = "name",
                entity = ShareClass,
                message = "Class name must be unique"
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
        validators = [ max_length(255) ]
    )
