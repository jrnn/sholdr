"""
    This module contains the blueprint for Certificate management endpoints.
    Certificates are funky so the views and operations are not vanilla CRUD.
"""

from app import (
    db,
    sql
)
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
    shares. The binding is done with two custom statements that handle several
    rows in one query; one for the join table, and another for updating the
    affected shares.
    """
    f = CertificateForm(request.form)
    if f.validate_on_submit():
        c = Certificate()
        f.populate_obj(c)
        c.share_count = c.last_share - c.first_share + 1

        db.session.add(c)
        db.session.commit()

        stmt1 = sql["CERTIFICATE"]["BUNDLE_JOIN"].params(
            id = c.id,
            l = c.first_share,
            u = c.last_share
        )
        stmt2 = sql["SHARE"]["BIND_RANGE"].params(
            l = c.first_share,
            u = c.last_share
        )
        db.engine.execute(stmt1)
        db.engine.execute(stmt2)
        db.commit_and_flush_cache()

        flash.create_ok("certificate")
        return redirect(url_for("share.list"))

    if request.method == "POST" and not f.validate():
        flash.invalid_input()

    return render_template(
        "certificate/form.html",
        form = f
    )
