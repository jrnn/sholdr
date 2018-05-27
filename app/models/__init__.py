from app.util.util import get_uuid
from flask_sqlalchemy import Model
from sqlalchemy import (
    Column,
    DateTime,
    func,
    String
)

class CustomModel(Model):
    """
    Centrally defines properties that are shared across all models. Namely,
    timestamps on creation and modification. Passed to SQLAlchemy when creating
    db instance.
    """
    created_on = Column(
        DateTime,
        default = func.current_timestamp()
    )
    updated_on = Column(
        DateTime,
        default = func.current_timestamp(),
        onupdate = func.current_timestamp()
    )

class UuidMixin(object):
    """
    Uses randomly generated UUIDs as primary key for models to which this is
    applied (chance of conflicts is infinitesimal). Not applied to all models,
    because it makes sense to identify e.g. Shares with sequential integers.

    Passed to affected models as constructor parameter alongside the default
    SQLAlchemy Model class.
    """
    id = Column(
        String(32),
        primary_key = True
    )

    def __init__(self):
        self.id = get_uuid()
