"""
    This module contains the Certificate model. A custom Mixin that generates
    UUIDs as primary keys is applied.

    In practice, Certificates are just bundles of sequential Shares. They are
    named after the first and last Share in the sequence (e.g. 001-050). A
    Certificate must contain every Share in between these two numbers.

    The purpose of Certificates is to enable ownership and trade of Shares in
    large numbers. So, all interactions between Shareholders and Shares are
    orchestrated through Certificates.

    Like Shares, Certificates are also a temporal entity, i.e. they can only be
    acted on between their dates of issuance and cancellation. Once canceled, a
    Certificate's Shares are released, which then may be bundled to new/other
    Certificate(s).

    The collection of Shares connected to a Certificate is fixed: therefore,
    Certificates memorize some key points about that relationship (first_share,
    last_share, share_count) to avoid having to query the DB over and again for
    the same unchanging information.
"""

import dateutil.parser as dtp

from .mixins import (
    BaseMixin,
    IssuableMixin,
    UuidMixin
)
from app import (
    cache,
    db,
    sql
)
from app.util.util import rs_to_dict
from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    String
)

# Join table handling many-to-many between Certificates and Shares
shares = db.Table(
    "certificate_share",
    Column(
        "share_id",
        BigInteger,
        ForeignKey("share.id")
    ),
    Column(
        "certificate_id",
        String(32),
        ForeignKey("certificate.id")
    )
)



class Certificate(BaseMixin, IssuableMixin, UuidMixin, db.Model):
    first_share = Column(
        BigInteger,
        nullable = False
    )
    last_share = Column(
        BigInteger,
        nullable = False
    )
    share_count = Column(
        BigInteger,
        nullable = False
    )

    shares = db.relationship(
        "Share",
        backref = db.backref(
            "certificate",
            lazy = True
        ),
        lazy = "subquery",
        secondary = shares
    )
    transactions = db.relationship(
        "Transaction",
        backref = db.backref(
            "certificate",
            lazy = True
        ),
        lazy = True
    )

    def get_status(self):
        if not self.canceled_on:
            return "Valid"
        else:
            return "Canceled"

    @staticmethod
    def bind_shares(certificate):
        """
        Handle the binding of a new certificate's (given as parameter) shares.
        This is done with two custom statements that process several rows in one
        query: one for updating the join table, and another for updating the
        'is_bound' flag of all affected shares.
        """
        stmt1 = sql["CERTIFICATE"]["BUNDLE_JOIN"].params(
            id = certificate.id,
            lower = certificate.first_share,
            upper = certificate.last_share
        )
        stmt2 = sql["SHARE"]["BIND_OR_RELEASE_RANGE"].params(
            is_bound = True,
            lower = certificate.first_share,
            upper = certificate.last_share
        )
        db.engine.execute(stmt1)
        db.engine.execute(stmt2)
        db.commit_and_flush_cache()

    @staticmethod
    def earliest_possible_bundle_date(lower, upper):
        """
        For the given range of shares, find:
          1. the latest cancellation date of all certificates those share have
             been part of;
          2. the latest issue date of those shares (by definition the issue date
             of the upper-bound share)
        and return the maximum of those dates. This is the earliest date that
        all the shares in the range exist and are unbound; in other words, the
        earliest date that it is logically possible to bind them together.
        """
        stmt = sql["CERTIFICATE"]["FIND_EARLIEST_BUNDLE_DATE"].params(
            lower = lower,
            upper = upper
        )
        rs = db.engine.execute(stmt).fetchone()

        if rs.max:
            return dtp.parse(rs.max).date()
        else:
            return None

    @staticmethod
    @cache.memoize()
    def get_current_owner(id):
        stmt = sql["CERTIFICATE"]["FIND_CURRENT_OWNER"].params(id = id)
        rs = db.engine.execute(stmt).fetchone()

        return { "id" : rs.id, "name" : rs.name }

    @staticmethod
    @cache.memoize()
    def get_latest_transaction_date(id):
        stmt = sql["_COMMON"]["FIND_MAX_WHERE"](
            table = "_transaction",
            column = "recorded_on",
            where = "certificate_id"
        ).params(value = id)
        rs = db.engine.execute(stmt).fetchone()

        if rs.max:
            return dtp.parse(rs.max).date()
        else:
            return None

    @staticmethod
    @cache.memoize()
    def get_share_composition_for(id):
        """
        Fetch the quantity and sum votes of shares bound to given certificate,
        broken down by share class.
        """
        stmt = sql["CERTIFICATE"]["CALCULATE_SHARE_COMPOSITION_FOR"].params(id = id)
        rs = db.engine.execute(stmt)

        return rs_to_dict(rs)

    @staticmethod
    @cache.cached(key_prefix = "certificate_list")
    def find_all_for_list():
        """
        Fetch all certificates for the list view. Use a custom aggregate JOIN
        query to include sum of votes per certificate in the result set.
        """
        stmt = sql["CERTIFICATE"]["FIND_ALL_FOR_LIST"]
        rs = db.engine.execute(stmt)

        return rs_to_dict(rs)

    @staticmethod
    def release_shares(certificate):
        """
        Release the range of shares bound to a canceled certificate (given as
        parameter) by setting the 'is_bound' flag of affected shares to 'false'.
        """
        stmt = sql["SHARE"]["BIND_OR_RELEASE_RANGE"].params(
            is_bound = False,
            lower = certificate.first_share,
            upper = certificate.last_share
        )
        db.engine.execute(stmt)
        db.commit_and_flush_cache()
