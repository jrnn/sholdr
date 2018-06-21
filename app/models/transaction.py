"""
    This module contains the Transaction model. Table name has extra underscore
    in front because TRANSACTION is a reserved SQL keyword.

    Transactions stand for events where ownership of a Certificate changes,
    recording (1) when the event takes place, (2) how much money is involved,
    and (3) who is selling and who is buying.

    Certificates can go through several Transactions during their validity.
    Certificates always know their current owner, but Transactions can tell the
    whole succession of owners over time.

    Transaction prices are of interest mainly when the issuing company is either
    the seller or buyer, because the difference in shares' purchase and buyback
    price has implications for the company's accounting and financial reporting.
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
from app.models.util import rs_to_dict_with_certificate_titles
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
    buyer_id = Column(
        String(32),
        ForeignKey("shareholder.id"),
        nullable = False
    )
    seller_id = Column(
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



    @staticmethod
    @cache.cached(key_prefix = "transaction_list")
    def get_all_for_list():
        """
        Fetch all transactions for the list view.
        """
        stmt = sql["TRANSACTION"]["FIND_ALL_FOR_LIST"]
        rs = db.engine.execute(stmt)

        return rs_to_dict_with_certificate_titles(rs, "title")



    @staticmethod
    @cache.memoize()
    def get_transaction_details(id):
        """
        Fetch the data of one transaction needed on the details page.
        """
        stmt = sql["TRANSACTION"]["FIND_DETAILS"].params(id = id)
        rs = db.engine.execute(stmt)
        t = rs_to_dict_with_certificate_titles(rs, "certificate")

        if not t:
            return None
        else:
            return t[0]
