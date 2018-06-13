"""
    This module contains the Shareholder model. A custom Mixin that generates
    UUIDs as primary keys is applied.

    Shareholders can be either natural persons (i.e. human beings) or juridical
    persons (i.e. organizations), with some differences in what information is
    needed for each. Though these differences are minor, for sake of practice,
    the two are treated as separate subclasses using joined table inheritance.

    Shareholders are also users of the application. Therefore the base class
    implements the methods required by flask-login. Email is used in place of
    username when logging in, possibly at some point also for verifying new
    users and/or resetting passwords.
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
    Boolean,
    Column,
    ForeignKey,
    String
)



class Shareholder(BaseMixin, UuidMixin, db.Model):
    email = Column(
        String(255),
        nullable = False,
        unique = True
    )
    pw_hash = Column(
        String(64),
        nullable = False
    )
    street = Column(
        String(255),
        nullable = False
    )
    street_ext = Column(String(255))
    zip_code = Column(
        String(32),
        nullable = False
    )
    city = Column(
        String(64),
        nullable = False
    )
    country = Column(
        String(64),
        nullable = False
    )
    has_access = Column(
        Boolean,
        default = True,
        nullable = False
    )
    is_admin = Column(
        Boolean,
        default = False,
        nullable = False
    )
    type = Column(String(16))

    transactions = db.relationship(
        "Transaction",
        backref = db.backref(
            "shareholder",
            lazy = True
        ),
        lazy = True
    )

    __mapper_args__ = {
        "polymorphic_identity" : "shareholder",
        "polymorphic_on" : type
    }

    def get_id(self):
        return self.id

    def is_active(self):
        return self.has_access

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def count_all():
        stmt = sql["_COMMON"]["COUNT_ALL"]("shareholder")
        rs = db.engine.execute(stmt).fetchone()

        return rs.count

    @staticmethod
    @cache.cached(key_prefix = "shareholder_list")
    def find_all_for_list():
        """
        Fetch all shareholders with only the fields needed on the list view.
        Need to do a bit of extra 'manual work' in translating query results
        due to subclassing ...
        """
        stmt = sql["SHAREHOLDER"]["FIND_ALL_FOR_LIST"]
        rs = db.engine.execute(stmt)
        ss = rs_to_dict(rs)

        for s in ss:
            s["type_id"] = s["business_id"]
            if s["type"] == "natural_person":
                s["name"] = "%s, %s" % (s["last_name"], s["first_name"],)
                s["type_id"] = s["nin"]
        return ss



class NaturalPerson(Shareholder):
    id = Column(
        String(32),
        ForeignKey("shareholder.id"),
        primary_key = True
    )
    first_name = Column(
        String(64),
        nullable = False
    )
    last_name = Column(
        String(64),
        nullable = False
    )
    nin = Column(   # National Identification Number
        String(16),
        nullable = False
    )
    nationality = Column(
        String(64),
        nullable = False
    )

    __mapper_args__ = {
        "polymorphic_identity" : "natural_person"
    }



class JuridicalPerson(Shareholder):
    id = Column(
        String(32),
        ForeignKey("shareholder.id"),
        primary_key = True
    )
    name = Column(
        String(128),
        nullable = False
    )
    business_id = Column(
        String(32),
        nullable = False,
        unique = True
    )
    contact_person = Column(
        String(128),
        nullable = False
    )

    __mapper_args__ = {
        "polymorphic_identity" : "juridical_person"
    }
