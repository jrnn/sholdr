"""
    This module contains custom and configured validators for use in WTForm
    classes.
"""

import datetime
import re

from app import db
from sqlalchemy import and_
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    ValidationError
)

def max_length(n = 255):
    return Length(
        max = n,
        message = "Max {} characters".format(n)
    )

class NinFormat(object):
    """
    Check that field value either consists of six digits, or matches the format
    of a Finnish HETU code (= national identification number).

    This is a very limited implementation, which does not detect e.g. days
    beyond 31 or months beyond 12, nor calculate the HETU checksum.
    """
    def __init__(self, message = None):
        if not message:
            message = "Give either date of birth as DDMMYY, or full Finnish HETU"
        self.message = message

    def __call__(self, form, field):
        nin = field.data
        dob = "^\d{6}$"
        hetu = "^\d{6}[A+-]\d{3}[0-9A-FHJ-NPR-Y]$"

        if not (re.match(dob, nin) or re.match(hetu, nin)):
            raise ValidationError(self.message)

def not_empty(message = "Cannot be empty"):
    return DataRequired(message)

class NotFuture(object):
    """
    Check that field value is not a future date.
    """
    def __init__(self, message = None):
        if not message:
            message = "Cannot be a future date"
        self.message = message

    def __call__(self, form, field):
        if not isinstance(field.data, datetime.date):
            raise ValidationError()
        if field.data > datetime.date.today():
            raise ValidationError("Cannot be in the future")

class PasswordFormat(object):
    """
    Check that field value only contains certain allowed characters; that it is
    at least 8 characters long; and that it has at least one of each: a capital
    letter, a small letter, and a number.
    """
    def __init__(self, message = None):
        if not message:
            message = "Does not meet password format requirements"
        self.message = message

    def __call__(self, form, field):
        pw = field.data
        allowed = "^[A-Za-z0-9!#$%&'*+.:,;/=?@^_~-]+$"
        reqs = "((?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,})"

        if not (re.match(allowed, pw) and re.match(reqs, pw)):
            raise ValidationError(self.message)

class RequiredIf(object):
    """
    Apply given validator only when some other field(s) have a certain value,
    e.g. ...Field('', [ RequiredIf(isNew = True, validator = DataRequired()) ]).
    """
    def __init__(self, validator, **kwargs):
        self.conds = kwargs
        self.validator = validator

    def __call__(self, form, field):
        for name, data in self.conds.items():
            other = form._fields.get(name)
            if other.data == data:
                self.validator()(form, field)
            Optional()(form, field)

class Unique(object):
    """
    Check that there are no rows in DB for given entity with field value in
    given column (excluding the current entity itself). For instance, check
    that given email address is not already reserved for any other user.
    """
    def __init__(self, column, entity, message = None):
        if not message:
            message = "Value already in use"

        self.entity = entity
        self.message = message
        self.unique_attr = getattr(entity, column)

    def __call__(self, form, field):
        if db.session.query(self.entity).filter(
            and_(
                self.entity.id != form.id.data,
                self.unique_attr == field.data
            )
        ).first():
            raise ValidationError(self.message)
