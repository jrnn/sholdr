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

    Shares are a temporal entity: they are valid only between their dates of
    issuance and cancellation. Once canceled, a Share no longer can be bound to
    a Certificate.
"""

from .mixins import IssuableMixin
from app import (
    cache,
    db,
    sql
)
from app.util.util import get_consecutive_ranges
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

    @staticmethod
    @cache.cached(key_prefix = "find_all_unbound")
    def get_unbound_ranges():
        """
        Return ranges of shares currently not bound to a certificate. The ranges
        are indicated as a list of tuples (a, b) where a = number of first and
        b = number of last share in range.
        """
        stmt = sql["SHARE"]["FIND_ALL_UNBOUND"]
        rs = db.engine.execute(stmt)

        return get_consecutive_ranges([ r.id for r in rs ])

    @staticmethod
    @cache.cached(key_prefix = "last_share_number")
    def last_share_number():
        """
        Return the id number up to which shares have been issued, or zero if no
        shares have been issued.
        """
        stmt = sql["SHARE"]["LAST_SHARE_NUMBER"]
        rs = db.engine.execute(stmt).fetchone()

        if not rs.max:
            return 0
        else:
            return rs.max
