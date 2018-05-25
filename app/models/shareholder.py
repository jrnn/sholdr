from . import UuidMixin
from app import db
from sqlalchemy import (
    Column,
    String
)

class Shareholder(UuidMixin, db.Model):
    """
    Note that Shareholders are also users of the application.
    """
    username = Column(
        String(16),
        nullable = False
    )
    pw_hash = Column(
        String(60),
        nullable = False
    )

    def __init__(self, username):
        self.username = username
        self.pw_hash = "kuha on varaani"
