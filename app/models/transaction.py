"""
    This module contains the Transaction model. A custom Mixin that generates
    UUIDs as primary keys is applied.

    Transactions stand for events where ownership of a Certificate changes,
    recording (1) when the event takes place, (2) how much money is involved,
    (3) to whom ownership is transferred.

    Certificates can go through several Transactions during their validity. The
    most recent Transaction tells which Shareholder that Certificate belongs to
    currently. When a Certificate is bundled, a 'trivial' Transaction at 0 EUR
    is written, just so that the Certificate initially has an owner.

    Transaction prices are of interest mainly when the issuing company is either
    the seller or buyer, because the difference in shares' purchase and buyback
    price has implications for the company's accounting and financial reporting.
"""

from .mixins import (
    BaseMixin,
    UuidMixin
)
from app import db
from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    String
)



class Transaction(BaseMixin, UuidMixin, db.Model):
    certificate_id = Column(
        String(32),
        ForeignKey("certificate.id"),
        nullable = False
    )
    shareholder_id = Column(
        String(32),
        ForeignKey("shareholder.id"),
        nullable = False
    )
    price = Column(
        BigInteger,
        default = 0
    )
    price_per_share = Column(
        BigInteger,
        default = 0
    )
    recorded_on = Column(
        Date,
        nullable = False
    )
    remarks = Column(String(255))

    __tablename__ = "_transaction"
