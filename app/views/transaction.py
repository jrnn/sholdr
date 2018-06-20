"""
    This module contains the blueprint for Transaction management endpoints.
    Because Transactions are created through Certificates and cannot be edited
    afterwards, the operations here are quite limited.
"""

from app.models.transaction import Transaction
from app.util.auth import login_required
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint(
    "transaction",
    __name__,
    url_prefix = "/transaction"
)



@bp.route("/", methods = ("GET",))
@login_required("ADMIN")
def list():
    """
    Show all transactions on a list.
    """
    return render_template(
        "transaction/list.html",
        transactions = Transaction.get_all_for_list()
    )
