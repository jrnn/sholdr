"""
    This module contains the blueprint for Share management endpoints. Shares
    are funky so the views and operations are not vanilla CRUD.
"""

from app import (
    cache,
    db
)
from app.forms.share import ShareIssueForm
from app.models.share import Share
from app.models.shareclass import ShareClass
from app.util import flash
from app.util.util import get_consecutive_ranges
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import login_required

bp = Blueprint(
    "share",
    __name__,
    url_prefix = "/share"
)

@bp.route("/", methods = ("GET",))
@login_required
def list():
    """
    Show the subindex for managing shares. (Okay it's not exactly a 'list' but
    for sake of naming consistency ...)
    """
    return render_template(
        "share/list.html",
        last_share_number = Share.last_share_number(),
        unbound_ranges = get_consecutive_ranges(Share.find_all_unbound())
    )

@bp.route("/new", methods = ("GET", "POST",))
@login_required
def issue():
    """
    Depending on request type, either (1) show blank form for issuing new
    shares; or (2) create new shares numbered X to Y, where X is the next 'free'
    integer in sequence and Y the given upper bound. If errors, throw back to
    form view.

    The form needs some data from DB (dynamic options for dropdown, current max
    share number). WTForms cannot handle these properly 'in-class', so the
    relevant queries are done here and filled in on each request. Also, GET and
    POST can in this case be handled neatly in a single function.
    """
    f = ShareIssueForm(request.form)
    l = Share.last_share_number() + 1

    f.lower_bound.data = l
    f.share_class_id.choices = [
        (s.id, "%s (%s votes / share)" % (s.name, s.votes),)
        for s in ShareClass.find_all_for_list()
    ]

    if f.validate_on_submit():
        for i in range(l, f.upper_bound.data + 1):
            s = Share()
            f.populate_obj(s)
            s.id = i
            db.session.add(s)

        db.session.commit()
        cache.clear()
        flash.create_ok("shares")
        return redirect(url_for("share.list"))

    if request.method == "POST" and not f.validate():
        flash.invalid_input()

    return render_template(
        "share/form.html",
        form = f
    )
