"""
    This module handles creation and configuration of the database connection;
    possible initialization of the database itself; and some base customization
    of the ORM model classes.
"""

from app.util.util import get_uuid
from flask_sqlalchemy import (
    Model,
    SQLAlchemy
)
from sqlalchemy import (
    Column,
    DateTime,
    func,
    String
)

def create_db(app):
    """
    Create and configure DB instance.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sholdr.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return SQLAlchemy(
        app,
        model_class = CustomModel
    )

def init_db(db):
    """
    Fetch all models and create DB tables accordingly, if none exist. Also, add
    one initial Shareholder to DB with which to handle the first login.
    """
    from . import shareholder

    try:
        db.create_all()
        create_initial_user(db)
    except:
        pass

class CustomModel(Model):
    """
    Centrally define properties that are shared across all models: namely,
    timestamps on creation and modification. Passed to SQLAlchemy when creating
    DB instance (above).
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
    Use randomly generated UUIDs as primary key for models to which this is
    applied (chance of conflicts is infinitesimal). Not applied to all models,
    because it makes sense to identify e.g. Shares with sequential integers.

    Pass to affected models as constructor parameter alongside the default
    SQLAlchemy Model class (or its derivative).
    """
    id = Column(
        String(32),
        primary_key = True
    )

    def __init__(self):
        self.id = get_uuid()

def create_initial_user(db):
    """
    If there are no Shareholders in DB, create a bullshit user just so that it
    is possible to log in. (Looking to replace this with something less hacky.)
    """
    from .shareholder import (
        NaturalPerson,
        Shareholder
    )

    if db.session.query(Shareholder).count() == 0:
        s = NaturalPerson()

        s.city = "Tayneville"
        s.country = "United Tims of Eric"
        s.email = "celery@man.io"
        s.first_name = "Celery"
        s.is_admin = True
        s.last_name = "Man"
        s.nationality = "United Tims of Eric"
        s.nin = "060469-433D"
        s.pw_hash = "$2b$12$z1rBZ0ymCMCQtcVeZL0Oyu1Zzs1ypPrDPG0IbMsnok4HwdjCm3yzm"
        s.street = "43D Flarhgunnstow Avenue"
        s.zip_code = "4D3D3D3"

        db.session.add(s)
        db.session.commit()
