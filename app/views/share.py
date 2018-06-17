"""
    This module contains the blueprint for Share management endpoints. Shares
    are funky so the views and operations are not vanilla CRUD.
"""

from app.forms.share import ShareForm
from app.models.certificate import Certificate
from app.models.share import Share
from app.models.shareclass import ShareClass
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
    "share",
    __name__,
    url_prefix = "/share"
)



@bp.route("/", methods = ("GET",))
@login_required("ADMIN")
def list():
    """
    Show the subindex for managing shares. (Okay it's not exactly a 'list' but
    for sake of naming consistency ...)
    """
    return render_template(
        "share/list.html",
        certificates = Certificate.get_all_for_list(),
        last_share_number = Share.get_last_share_number(),
        unbound_ranges = Share.get_unbound_ranges()
    )



@bp.route("/new", methods = ("GET", "POST",))
@login_required("ADMIN")
def issue():
    """
    Depending on request type, either (1) show blank form for issuing new
    shares; or (2) create new shares numbered X to Y, where X is the next 'free'
    integer in sequence and Y the given upper bound.

    The form needs some data from DB (dynamic options for dropdown, current max
    share number, etc.) WTForms cannot handle these properly 'in-class', so the
    relevant queries are done here and filled in on each request.
    """
    f = ShareForm(request.form)
    lower = Share.get_last_share_number() + 1

    f.latest_issue.data = Share.get_latest_issue_date()
    f.lower_bound.data = lower
    f.share_class_id.choices = ShareClass.get_dropdown_options()

    if f.validate_on_submit():
        Share.issue_from_form(f)
        notify.create_ok("shares")
        return redirect(url_for("share.list"))

    elif request.method == "POST":
        notify.invalid_input()

    return render_template(
        "share/form.html",
        form = f
    )
