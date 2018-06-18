"""
    This module contains the blueprint for Share Class management endpoints,
    spanning the standard CRUD operations.
"""

from app.forms.shareclass import ShareClassForm
from app.models.shareclass import ShareClass
from app.util import notify
from app.util.auth import login_required
from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint(
    "shareclass",
    __name__,
    url_prefix = "/shareclass"
)



@bp.route("/", methods = ("GET",))
@login_required("ADMIN")
def list():
    """
    Show all share classes on a list.
    """
    return render_template(
        "shareclass/list.html",
        shareclasses = ShareClass.get_all_for_list()
    )



@bp.route("/<id>", methods = ("GET",))
@login_required("ADMIN")
def form(id):
    """
    Find share class by given primary key (path variable), and show form
    prefilled with its data. If value "new" is given, show empty form instead.
    """
    if id == "new":
        f = ShareClassForm()
    else:
        s = ShareClass.query.get_or_404(id)
        f = ShareClassForm(obj = s)

    return render_template(
        "shareclass/form.html",
        form = f
    )



@bp.route("/", methods = ("POST",))
@login_required("ADMIN")
def create_or_update():
    """
    Either create a new share class or update existing one, depending on whether
    there is a record in DB for given primary key (passed as hidden form field).
    """
    f = ShareClassForm(request.form)
    id = f.id.data

    if not f.validate():
        notify.invalid_input()
        return render_template(
            "shareclass/form.html",
            form = f
        )

    del f.id # avoid overwriting id = 'new' when creating new
    s = ShareClass.query.get_or_default(id, ShareClass())
    f.populate_obj(s)
    s.save_or_update()

    if id == "new":
        notify.create_ok("share class")
    else:
        notify.update_ok("share class")
    return redirect(url_for("shareclass.list"))



@bp.route("/<id>/delete", methods = ("POST",))
@login_required("ADMIN")
def delete(id):
    """
    Delete share class by primary key (path variable), if found. Otherwise throw
    404. Refuse to delete share class that is bound to at least one share.
    """
    if ShareClass.count_shares_in_class(id):
        notify.delete_error("share class", "share")
        return redirect(url_for("shareclass.list"))

    if not ShareClass.query.get(id).delete_if_exists():
        abort(404)

    notify.delete_ok("share class")
    return redirect(url_for("shareclass.list"))
