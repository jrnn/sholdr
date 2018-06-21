"""
    This module contains utility functions needed by more than one model class
    (currently only one such function). The only reason for having this as a
    separate module is that trying to stuff the function either into /util/util
    or /models/__init__ causes cyclical dependencies, which seems to suggest
    that the way I've organized my code is somehow flawed.
"""

from app.models.share import Share
from app.util.util import (
    format_share_range,
    rs_to_dict
)



def rs_to_dict_with_certificate_titles(rs, key):
    """
    Takes a query resultproxy, expecting that 'first_share' and 'last_share' are
    among the columns, converts the rows to dicts, and finally writes in
    certificate titles to each dict (under given key) in a standard format.

    This is best thought of as an extension of the more generic 'rs_to_dict'
    utility function for cases where certificate titles are needed.
    """
    entities = rs_to_dict(rs)
    places = len(str(Share.get_last_share_number()))

    for e in entities:
        e.update({ key : format_share_range(
            lower = e["first_share"],
            upper = e["last_share"],
            places = places
        ) })

    return entities
