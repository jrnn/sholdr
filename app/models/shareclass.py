"""
    This module contains the Share Class model. A custom Mixin that generates
    UUIDs as primary keys is applied.

    Share Classes are used to categorize Shares in terms of privilege: that is,
    Shares of different Classes confer different rights to their owner. For the
    purposes of this app, Share Class just quantifies voting rights.
"""

from . import UuidMixin
from app import db
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
