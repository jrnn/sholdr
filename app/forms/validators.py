"""
    This module contains custom and configured validators for use in WTForm
    classes. Explanations are not given in cases where the class name is self-
    explanatory.
"""

import datetime
import re

from app import (
    db,
    sql
)
from app.models.certificate import Certificate
from app.models.share import Share
from app.util.util import is_within_range
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



class NotEarlierThan(object):
    def __init__(self, earlier, message = None):
        if not message:
            message = "Cannot be earlier than %s" % earlier.lower()
        self.earlier = earlier
        self.message = message

    def __call__(self, form, field):
        if not isinstance(field.data, datetime.date):
            pass
        elif field.data < form._fields.get(self.earlier).data:
            raise ValidationError(self.message)



class NotEmpty(object):
    def __call__(self, form, field):
        DataRequired("Cannot be empty")(form, field)



class NotEqualTo(object):
    def __init__(self, other, message = None):
        if not message:
            message = "Cannot be same as %s" % other.lower()
        self.message = message
        self.other = other

    def __call__(self, form, field):
        try:
            other = form[self.other]
        except:
            raise ValidationError("Field %s does not exist!" % self.other)
        if field.data == other.data:
            raise ValidationError(self.message)



class NotFutureDate(object):
    def __call__(self, form, field):
        if not isinstance(field.data, datetime.date):
            pass
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
        allowed = "^[A-Za-z0-9!#$%&'*+.:,;/=?@^_~-]+$"
        reqs = "((?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,})"

        if not (re.match(allowed, field.data) and re.match(reqs, field.data)):
            raise ValidationError(self.message)



class PossibleBundleDate(object):
    """
    This validator is only meant to be used by the Certificate form. It checks
    that the given issue date (1) does not overlap with possible prior bindings
    of the shares, (2) does not precede the issue date of any of the shares.

    The actual work is done by the Certificate model class, while this validator
    just collects relevant values together and typechecks them.
    """
    def __call__(self, form, field):
        date = field.data
        lower = form._fields.get("first_share").data
        upper = form._fields.get("last_share").data

        if type(lower) != int or type(upper) != int or not isinstance(date, datetime.date):
            return
        elif lower > upper:
            return

        earliest = Certificate.get_earliest_possible_bundle_date(lower, upper)
        if earliest and date < earliest:
            raise ValidationError("Earliest possible date is %s" % earliest)



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
    def __init__(self, column, table, message = None):
        if not message:
            message = "Value already in use"
        self.message = message
        self.stmt = sql["_COMMON"]["CHECK_IF_UNIQUE"](table, column)

    def __call__(self, form, field):
        stmt = self.stmt.params(
            id = form.id.data,
            unique_value = field.data
        )
        rs = db.engine.execute(stmt).fetchone()
        if rs.count:
            raise ValidationError(self.message)



class WithinBounds(object):
    """
    This validator is only meant to be used by the Certificate form. It does a
    number of checks on given integer pair, ensuring that they are within bounds
    of issued shares, and that all the shares within that range currently are
    not bound to another Certificate.
    """
    def __call__(self, form, field):
        lower = form.first_share.data
        upper = field.data

        if type(lower) != int or type(upper) != int:
            raise ValidationError("Not a valid integer value")
        elif upper < lower:
            raise ValidationError("Upper bound must be greater than lower bound (idiot...)")
        elif lower < 1:
            raise ValidationError("Numbering of shares starts from 1")

        cap = Share.get_last_share_number()
        if upper > cap:
            raise ValidationError("Shares have only been issued up to %s" % cap)
        elif not is_within_range((lower,upper,), Share.get_unbound_ranges()):
            raise ValidationError("One or more shares within this range is already bound to a certificate")
