"""
    This module contains the Share model. Unlike other models, Shares use
    sequential integers as the primary key, because this is how they are
    identified and named in real life as well.

    Shares are THE key concept of the app, however they hold very little
    information or functionality. An individual Share is hardly interesting at
    all; rather, they become pertinent on an aggregate level. In practice, all
    Share interactions happen via Certificates, which is another model and a
    kind of 'container' class for Shares.

    The only reason Share is distinguished as a model in its own right, is that
    Certificates are not fixed over time (if they were, this would be soooo much
    simpler...) i.e. one Share can over time "move" between Certificates.

    Shares are a temporal entity -- they are valid only between their dates of
    issuance and cancellation. Once canceled, a Share no longer can be bound to
    a Certificate.
"""

from . import IssuableMixin
from app import db
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    String
)

class Share(IssuableMixin, db.Model):
    id = Column(
        BigInteger,
        primary_key = True
    )
    is_bound = Column(
        Boolean,
        default = False,
        nullable = False
    )
    share_class_id = Column(
        String(32),
        ForeignKey("share_class.id"),
        nullable = False
    )
    ## possibly add 'nominal_value' ?
