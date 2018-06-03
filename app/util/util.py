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

def get_uuid():
    """
    Returns a v4 UUID as string without dashes in the middle.
    """
    return re.sub(
        "-",
        "",
        str(uuid.uuid4())
    )
