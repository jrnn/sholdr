"""
    This module contains the blueprint for Certificate management endpoints.
    Certificates are funky so the views and operations are not vanilla CRUD.
"""

from app.forms.certificate import CertificateForm
from app.models.certificate import Certificate
from app.util import flash
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
    shares.
    """
    f = CertificateForm(request.form)

    if f.validate_on_submit():
        c = Certificate()
        f.populate_obj(c)
        c.share_count = c.last_share - c.first_share + 1

        c.save_or_update()
        Certificate.bind_shares(c)

        flash.create_ok("certificate")
        return redirect(url_for("share.list"))

    if request.method == "POST" and not f.validate():
        flash.invalid_input()

    return render_template(
        "certificate/form.html",
        form = f
    )



@bp.route("/<id>", methods = ("GET",))
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
        share_classes = sc,
        total_votes = sum([ s["votes"] for s in sc ])
    )



@bp.route("/<id>", methods = ("POST",))
def cancel(id):
    return "not yet implemented, hefe"
