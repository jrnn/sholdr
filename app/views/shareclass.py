"""
    This module contains the blueprint for Share Class management endpoints,
    spanning the standard CRUD operations.
"""

from app import db
from app.forms.shareclass import ShareClassForm
from app.models.shareclass import ShareClass
from app.util import flash
from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import login_required

bp = Blueprint(
    "shareclass",
    __name__,
    url_prefix = "/shareclass"
)

@bp.route("/", methods = ("GET",))
@login_required
def list():
    """
    Show all share classes on a list.
    """
    return render_template(
        "shareclass/list.html",
        shareclasses = ShareClass.find_all_for_list()
    )

@bp.route("/<id>", methods = ("GET",))
@login_required
def form(id):
    """
    Find one share class by primary key (given as path variable), and show form
    prefilled with its data.

    If the value "new" is given, show empty form instead.

    In either case the same html template is used. The id value is passed to the
    form as a hidden prop, which allows the function handling the submit to
    decide whether to create new share class or update existing one.
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
@login_required
def create_or_update():
    """
    Either create a new share class or update existing one, depending on the
    inbound form's id field (process is very similar in both cases).
    """
    id = request.form.get("id")

    f = ShareClassForm(request.form)
    if not f.validate():
        flash.invalid_input()
        return render_template(
            "shareclass/form.html",
            form = f
        )

    s = ShareClass.query.get_or_default(id, ShareClass())
    del f.id  # avoid setting "new" as pk when creating new share class
    f.populate_obj(s)

    if id == "new":
        db.session.add(s)
        flash.create_ok("share class")
    else:
        flash.update_ok("share class")

    db.commit_and_flush_cache()
    return redirect(url_for("shareclass.list"))

@bp.route("/<id>/delete", methods = ("POST",))
@login_required
def delete(id):
    """
    Delete share class by primary key (given as path variable), if found.
    Otherwise throw 404.
    """
    if not ShareClass.query.filter_by(id = id).delete():
        abort(404)

    db.commit_and_flush_cache()
    flash.delete_ok("share class")
    return redirect(url_for("shareclass.list"))
