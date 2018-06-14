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
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import login_required

bp = Blueprint(
    "certificate",
    __name__,
    url_prefix = "/certificate"
)



@bp.route("/", methods = ("GET", "POST",))
@login_required
def bundle():
    """
    Depending on request type, either (1) show blank form for bundling shares
    into certificates, or (2) create new certificate and bind its component
    shares, then create a trivial transaction naming the initial owner.
    """
    f = CertificateForm(request.form)
    f.shareholder_id.choices = Shareholder.get_dropdown_options()

    if f.validate_on_submit():
        c = Certificate()
        f.populate_obj(c)
        c.share_count = c.last_share - c.first_share + 1

        c.save_or_update()
        Certificate.bind_shares(c)

        t = Transaction()
        t.certificate_id = c.id
        t.shareholder_id = f.shareholder_id.data
        t.recorded_on = f.issued_on.data
        t.save_or_update()

        notify.create_ok("certificate")
        return redirect(url_for("share.list"))

    elif request.method == "POST":
        notify.invalid_input()

    return render_template(
        "certificate/form.html",
        form = f
    )



@bp.route("/<id>", methods = ("GET",))
@login_required
def details(id):
    """
    Show page with certificate basic information, share composition breakdown by
    share class, and transaction history.
    """
    c = Certificate.query.get_or_404(id)
    sc = Certificate.get_share_composition_for(id)

    return render_template(
        "certificate/details.html",
        certificate = c,
        current_owner = Certificate.get_current_owner(id),
        share_classes = sc,
        total_votes = sum([ s["votes"] for s in sc ])
    )



@bp.route("/<id>/transfer", methods = ("GET", "POST",))
@login_required
def transfer(id):
    """
    Depending on request type, either (1) show blank form for recording a
    transaction, or (2) create new transaction. Refuse to do anything if the
    certificate in question has been canceled.
    """
    c = Certificate.query.get_or_404(id)

    if c.canceled_on:
        notify.has_been_canceled("certificate")
        return redirect(url_for("certificate.details", id = id))

    f = TransactionForm(request.form)
    f.shareholder_id.choices = Shareholder.get_dropdown_options()

    if f.validate_on_submit():
        t = Transaction()
        f.populate_obj(t)

        t.price = int(100 * t.price)
        t.price_per_share = int(t.price / c.share_count)
        t.save_or_update()

        notify.create_ok("transaction")
        return redirect(url_for("certificate.details", id = id))

    elif request.method == "POST":
        notify.invalid_input()

    else:
        f.certificate_id.data = id
        f.shares.data = "%s—%s" % (c.first_share, c.last_share,)

        current_owner = Certificate.get_current_owner(id)
        f.owner.data = current_owner.get("name")
        f.owner_id.data = current_owner.get("id")
        f.latest_transaction.data = Certificate.get_latest_transaction_date(id)

    return render_template(
        "transaction/form.html",
        form = f
    )



@bp.route("/<id>/cancel", methods = ("GET", "POST",))
@login_required
def cancel(id):
    """
    Practically the opposite of 'bundle()' above. Refuse to do anything if the
    certificate in question has been canceled already.
    """
    c = Certificate.query.get_or_404(id)
    f = CancellationForm(request.form)

    if c.canceled_on:
        notify.has_been_canceled("certificate")
        return redirect(url_for("certificate.details", id = id))

    if f.validate_on_submit():
        c.canceled_on = f.canceled_on.data
        Certificate.release_shares(c)

        notify.cancel_ok("certificate")
        return redirect(url_for("share.list"))

    elif request.method == "POST":
        notify.invalid_input()

    else:
        f = CancellationForm(obj = c)
        f.shares.data = "%s—%s" % (c.first_share, c.last_share,)
        f.latest_transaction.data = Certificate.get_latest_transaction_date(id)

    return render_template(
        "certificate/cancel.html",
        form = f
    )
