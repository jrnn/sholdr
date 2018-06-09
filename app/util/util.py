"""
    This module contains generic utility functions that are needed here and
    there.

    The several 'apply'-something functions below seem trivial, but they are
    needed for WTForm transformations (passed into a field as 'filters').
"""

import re
import uuid



def apply_lower(s):
    """
    Apply .lower() to given value if applicable.
    """
    if s is not None and hasattr(s, "lower"):
        return s.lower()
    else:
        return s



def apply_strip(s):
    """
    Apply .strip() to given value if applicable.
    """
    if s is not None and hasattr(s, "strip"):
        return s.strip()
    else:
        return s



def apply_upper(s):
    """
    Apply .upper() to given value if applicable.
    """
    if s is not None and hasattr(s, "upper"):
        return s.upper()
    else:
        return s



def get_consecutive_ranges(ns):
    """
    Find all ranges of consecutive numbers from a _SORTED_ integer list. Return
    the first and last numbers of each range as a tuple (first, last).
    """
    res = []
    if not ns:
        return res

    prev = first = ns[0] - 2
    for n in ns:
        if n != prev + 1:
            if prev != ns[0] - 2:
                res.append( (first, prev,) )
            first = n
        prev = n

    res.append( (first, prev,) )
    return res



def get_uuid():
    """
    Return a v4 UUID as string without dashes in the middle.
    """
    return re.sub(
        "-",
        "",
        str(uuid.uuid4())
    )



def is_within_range(t, ts):
    """
    Check whether the given integer pair (t) is within at least one of the given
    ranges (ts). t must be a tuple, and ts a list of tuples.
    """
    (a, b,) = t
    for (l, u,) in ts:
        if l <= a and b <= u:
            return True
    return False



def rs_to_dict(rs):
    """
    Iterate through a ResultProxy, translate each row into a dictionary with the
    exact same keys as the ResultProxy, and return the dictionaries as a list.
    """
    res = []
    for r in rs:
        res.append({ key : r[key] for key in rs.keys() })
    return res
