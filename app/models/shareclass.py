"""
    This module contains the Share Class model.

    Share Classes are used to categorize Shares in terms of privilege: that is,
    Shares of different Classes confer different rights to their owner. For the
    purposes of this app, Share Class just quantifies voting rights.
"""

from .mixins import (
    BaseMixin,
    UuidMixin
)
from app import (
    cache,
    db,
    sql
)
from app.util.util import rs_to_dict
from sqlalchemy import (
    Column,
    Integer,
    String
)



class ShareClass(BaseMixin, UuidMixin, db.Model):
    name = Column(
        String(32),
        nullable = False,
        unique = True
    )
    votes = Column(
        Integer,
        default = 1,
        nullable = False
    )
    remarks = Column(String(255))

    @staticmethod
    def count_shares_in_class(id):
        stmt = sql["_COMMON"]["COUNT_WHERE"]("share", "share_class_id")
        rs = db.engine.execute(stmt.params(value = id)).fetchone()

        return rs.count

    @staticmethod
    @cache.cached(key_prefix = "share_class_list")
    def get_all_for_list():
        """
        Fetch all share classes for the list view, including number of shares
        per class.
        """
        stmt = sql["SHARE_CLASS"]["FIND_ALL_FOR_LIST"]
        rs = db.engine.execute(stmt)

        return rs_to_dict(rs)

    @staticmethod
    @cache.cached(key_prefix = "share_class_dropdown")
    def get_dropdown_options():
        """
        Fetch all share classes with a simple query, and return an array of
        (value, label) tuples for use as dropdown options.
        """
        return [
            (s.id, "%s (%s votes / share)" % (s.name, s.votes),)
            for s in db.engine.execute(sql["SHARE_CLASS"]["FIND_ALL_FOR_DROPDOWN"])
        ]
