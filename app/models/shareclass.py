"""
    This module contains the Share Class model. A custom Mixin that generates
    UUIDs as primary keys is applied.

    Share Classes are used to categorize Shares in terms of privilege: that is,
    Shares of different Classes confer different rights to their owner. For the
    purposes of this app, Share Class just quantifies voting rights.
"""

from . import UuidMixin
from app import (
    cache,
    db,
    queries
)
from app.util.util import rs_to_dict
from sqlalchemy import (
    Column,
    Integer,
    String
)

class ShareClass(UuidMixin, db.Model):
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

    shares = db.relationship(
        "Share",
        backref = db.backref(
            "share_class",
            lazy = True
        ),
        lazy = True
    )

    @staticmethod
    def count_shares_for(id):
        q = queries["SHARE_CLASS"]["COUNT_SHARES_FOR"].params(id = id)
        rs = db.engine.execute(q).fetchone()

        return rs.count

    @staticmethod
    @cache.cached(key_prefix = "share_class_dropdown")
    def find_all_for_dropdown():
        """
        Fetch all share classes (simple query) and return an array of (value,
        label) tuples for use as dropdown options.
        """
        q = queries["SHARE_CLASS"]["FIND_ALL_FOR_DROPDOWN"]

        return [
            (s.id, "%s (%s votes / share)" % (s.name, s.votes),)
            for s in db.engine.execute(q)
        ]

    @staticmethod
    @cache.cached(key_prefix = "share_class_list")
    def find_all_for_list():
        """
        Fetch all share classes for the list view. Use a custom aggregate join
        query to include number of shares per class in the result set.
        """
        q = queries["SHARE_CLASS"]["FIND_ALL_FOR_LIST"]
        rs = db.engine.execute(q)

        return rs_to_dict(rs)
