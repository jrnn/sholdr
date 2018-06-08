"""
    This module contains custom and configured validators for use in WTForm
    classes. Explanations are not given in cases where the class name is self-
    explanatory.
"""

import datetime
import re

from app import db
from app.models.share import Share
from app.util.util import (
    get_consecutive_ranges,
    is_within_range
)
from sqlalchemy import and_
from wtforms.validators import (
    DataRequired,
    Optional,
    ValidationError
)

class MaxLength(object):
    def __init__(self, max, message = None):
        if not message:
            message = "Maximum %s characters" % max
        self.max = max
        self.message = message

    def __call__(self, form, field):
        s = field.data.strip()
        if len(s) > self.max:
            raise ValidationError(self.message)

class NinFormat(object):
    """
    Check that field value either is a valid date DDMMYY, or matches the format
    of a Finnish HETU code (= national identification number).

    Impossible dates are detected, however without accounting for leap years.
    HETU part is validated for format only, i.e. checksum is not calculated.
    """
    def __init__(self, message = None):
        if not message:
            message = "Give either date of birth as DDMMYY, or full Finnish HETU"
        self.message = message

    def __call__(self, form, field):
        s = field.data.strip()
        ddmmyy = "^(31(0[13578]|1[02]))|(30(0[13-9]|1[012]))|((0[1-9]|[12][0-9])(0[1-9]|1[012]))\d\d$"
        hetu = "^[A+-]\d{3}[0-9A-FHJ-NPR-Y]$"

        if len(s) == 6 and re.match(ddmmyy, s):
            return
        elif re.match(ddmmyy, s[:6]) and re.match(hetu, s[6:]):
            return
        raise ValidationError(self.message)

class NotEmpty(object):
    def __call__(self, form, field):
        DataRequired("Cannot be empty")(form, field)

class NotFutureDate(object):
    def __call__(self, form, field):
        if not isinstance(field.data, datetime.date):
            raise ValidationError()
        elif field.data > datetime.date.today():
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

class WithinBounds(object):
    """
    This validator is only meant to be used by the Certificate form. It does a
    number of checks on given integer pair, ensuring that they are within bounds
    of issued shares, and that all the shares within that range currently are
    not bound to another Certificate.
    """
    def __call__(self, form, field):
        l = form.first_share.data
        u = field.data

        if type(l) != int or type(u) != int:
            raise ValidationError()
        if u < l:
            raise ValidationError("Upper bound must be greater than lower bound (idiot...)")

        m = Share.last_share_number()
        if u > m:
            raise ValidationError("Shares have only been issued up to %s" % m)
        if l < 1:
            raise ValidationError("Numbering of shares starts from 1")

        unbound_ranges = get_consecutive_ranges(Share.find_all_unbound())
        if not is_within_range( (l,u,), unbound_ranges):
            raise ValidationError("One or more shares within this range is already bound to a certificate")
