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
    Certificate's Shares are unbound, which then may be bundled to new/other
    Certificate(s).

    The collection of Shares connected to a Certificate is fixed: therefore,
    Certificates memorize some key points about that relationship (first_share,
    last_share, share_count) to avoid having to query the DB over and again for
    the same unchanging information.
"""

from . import (
    IssuableMixin,
    UuidMixin
)
from app import db
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

class Certificate(IssuableMixin, UuidMixin, db.Model):
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
            "certificates",
            lazy = True
        ),
        lazy = "subquery",
        secondary = shares
    )

    def get_name(self):
        return self.first_share + "—" + self.last_share
