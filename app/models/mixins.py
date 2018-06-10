"""
    This module contains custom Mixins that define functionality that is useful
    in more than one Model class.
"""

from app import db
from app.util.util import get_uuid
from sqlalchemy import (
    Column,
    Date,
    inspect,
    String
)



class BaseMixin(object):
    """
    Using SQLAlchemy state management, do basic CRUD operations with instance in
    question, based on its 'object state'. 'Transient' roughly means the same as
    'isNew = true'; 'persistent' means that instance has record in DB.
    """
    def delete_if_exists(self):
        if inspect(self).persistent:
            db.session.delete(self)
            db.commit_and_flush_cache()
            return True
        return False

    def save_or_update(self):
        if inspect(self).transient:
            db.session.add(self)
        db.commit_and_flush_cache()



class IssuableMixin(object):
    """
    Add columns for issue and cancellation dates (simple enough...)
    """
    canceled_on = Column(Date)
    issued_on = Column(
        Date,
        nullable = False
    )



class UuidMixin(object):
    """
    Use randomly generated UUIDs as primary key for models to which this is
    applied (chance of conflicts is infinitesimal).
    """
    id = Column(
        String(32),
        primary_key = True
    )

    def __init__(self):
        self.id = get_uuid()
