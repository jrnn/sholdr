from . import UuidMixin
from app import db
from sqlalchemy import (
    Column,
    ForeignKey,
    String
)

class Shareholder(UuidMixin, db.Model):
    """
    Note that Shareholders are also users of the application. Email is used in
    place of username when logging in, and also for verifying new users and/or
    resetting password.

    Shareholders can be either natural persons (i.e. human beings) or juridical
    persons (i.e. organizations), with some differences in what information is
    needed for each. Though these differences are minor, for sake of practice,
    the two are treated as separate subclasses using joined table inheritance.
    """
    email = Column(
        String(255),
        nullable = False,
        unique = True
    )
    pw_hash = Column(
        String(60),
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
    # add later
    #  - authority (basic vs. admin user)
    #  - access rights (boolean)
    type = Column(String(16))
    __mapper_args__ = {
        "polymorphic_identity" : "shareholder",
        "polymorphic_on" : type
    }

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

    def get_name(self):
        return self.last_name + ", " + self.first_name

    def get_id(self):
        return self.nin

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

    def get_name(self):
        return self.name

    def get_id(self):
        return self.business_id
