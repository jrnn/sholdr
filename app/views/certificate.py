"""
    This module contains the blueprint for Certificate management endpoints.
    Certificates are funky so the views and operations are not vanilla CRUD.
"""

from app.forms.certificate import (
    CancellationForm,
    CertificateForm
)
from app.forms.transaction import TransactionForm
from app.models.certificate import Certificate
from app.models.shareholder import Shareholder
from app.models.transaction import Transaction
from app.util import notify
from app.util.auth import login_required
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint(
    "certificate",
    __name__,
    url_prefix = "/certificate"
)



@bp.route("/", methods = ("GET", "POST",))
@login_required("ADMIN")
def bundle():
    """
    Depending on request type, either (1) show form for bundling shares into
    certificates, or (2) create new certificate and bind its component shares.
    """
    f = CertificateForm(request.form)
    f.owner_id.choices = Shareholder.get_dropdown_options()

    if f.validate_on_submit():
        c = Certificate()
        f.populate_obj(c)
        c.share_count = c.last_share - c.first_share + 1

        c.save_or_update()
        Certificate.bind_shares(c)

        notify.create_ok("certificate")
        return redirect(url_for("share.list"))

    elif request.method == "POST":
        notify.invalid_input()

    return render_template(
        "certificate/form.html",
        form = f
    )



@bp.route("/<id>", methods = ("GET",))
@login_required("ADMIN")
def details(id):
    """
    Show page with certificate basic information, share composition breakdown by
    share class, and transaction history.
    """
    certificate = Certificate.query.get_or_404(id)
    shareclasses = Certificate.get_share_composition(id)

    return render_template(
        "certificate/details.html",
        certificate = certificate,
        current_owner = Certificate.get_current_owner(id),
        shareclasses = shareclasses,
        total_votes = sum([ s["votes"] for s in shareclasses ]),
        transactions = Certificate.get_transactions(id)
    )



@bp.route("/<id>/transfer", methods = ("GET", "POST",))
@login_required("ADMIN")
def transfer(id):
    """
    Depending on request type, either (1) show form for recording a transaction,
    or (2) create new transaction, and update 'current owner' field on the
    certificate. Refuse to do anything if the certificate in question already
    has been canceled.
    """
    c = Certificate.query.get_or_404(id)
    if c.canceled_on:
        notify.is_already_canceled("certificate")
        return redirect(url_for("certificate.details", id = id))

    f = TransactionForm(request.form)
    f.buyer_id.choices = Shareholder.get_dropdown_options()

    if f.validate_on_submit():
        t = Transaction()
        f.populate_obj(t)

        c.owner_id = f.buyer_id.data
        t.price = int(100 * t.price)
        t.price_per_share = int(t.price / c.share_count)
        t.save_or_update()

        notify.create_ok("transaction")
        return redirect(url_for("certificate.details", id = id))

    elif request.method == "POST":
        notify.invalid_input()

    else:
        f.certificate_id.data = id
        f.shares.data = c.get_title()

        f.seller_id.data = c.owner_id
        f.seller.data = Certificate.get_current_owner(id).get("name")
        f.last_transaction.data = Certificate.get_last_transaction_date(id) \
                                  or c.issued_on

    return render_template(
        "transaction/form.html",
        form = f
    )



@bp.route("/<id>/cancel", methods = ("GET", "POST",))
@login_required("ADMIN")
def cancel(id):
    """
    Depending on request type, either (1) show form for canceling certificate,
    or (2) cancel certificate and release its component shares. Refuse to do
    anything if the certificate in question already has been canceled.
    """
    c = Certificate.query.get_or_404(id)
    if c.canceled_on:
        notify.is_already_canceled("certificate")
        return redirect(url_for("certificate.details", id = id))

    f = CancellationForm(request.form)
    if f.validate_on_submit():
        c.canceled_on = f.canceled_on.data
        Certificate.release_shares(c)

        notify.cancel_ok("certificate")
        return redirect(url_for("share.list"))

    elif request.method == "POST":
        notify.invalid_input()

    else:
        f = CancellationForm(obj = c)
        f.shares.data = c.get_title()
        f.last_transaction.data = Certificate.get_last_transaction_date(id) \
                                  or c.issued_on

    return render_template(
        "certificate/cancel.html",
        form = f
    )
