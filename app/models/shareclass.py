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
    db
)
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

    @staticmethod
    @cache.cached(key_prefix = "share_class_list")
    def find_all_for_list():
        """
        Probably no need to use manual query... This is here only so that query
        result can be cached without also caching other view-related effects
        (e.g. flashed messages).
        """
        return db.session.query(ShareClass).all()
