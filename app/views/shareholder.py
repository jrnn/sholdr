"""
    This module contains the blueprint for Shareholder management endpoints,
    spanning the standard CRUD operations. Because Shareholders come in two
    flavors (subclassing), the code is a bit bulkier than usual.
"""

from app.forms.shareholder import (
    JuridicalPersonForm,
    NaturalPersonForm
)
from app.models.shareholder import (
    JuridicalPerson,
    NaturalPerson,
    Shareholder
)
from app.util import flash
from app.util.auth import hashPassword
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
    "shareholder",
    __name__,
    url_prefix = "/shareholder"
)



@bp.route("/", methods = ("GET",))
@login_required
def list():
    """
    Show all shareholders on a list.
    """
    return render_template(
        "shareholder/list.html",
        shareholders = Shareholder.find_all_for_list()
    )



@bp.route("/<id>", methods = ("GET",))
@login_required
def form(id):
    """
    Find shareholder by given primary key (path variable), then query for the
    correct subclass entity by type, and finally show corresponding form
    prefilled with its data.

    If value "new" is given, show empty form instead. Shareholder type must be
    given as query parameter, so that the correct WTForm class is passed to
    Jinja. If an incorrect or no type is given, redirect to list view.
    """
    if id == "new":
        type = request.args.get("type")

        if type == "natural":
            f = NaturalPersonForm()
        elif type == "juridical":
            f = JuridicalPersonForm()
        else:
            flash.incorrect_type("shareholder")
            return redirect(url_for("shareholder.list"))
        f.is_new.data = True

    else:
        s = Shareholder.query.get_or_404(id)

        if s.type == "natural_person":
            s = NaturalPerson.query.get(id)
            f = NaturalPersonForm(obj = s)
        else:
            s = JuridicalPerson.query.get(id)
            f = JuridicalPersonForm(obj = s)

    return render_template(
        "shareholder/form.html",
        form = f,
        id = id
    )



@bp.route("/<id>", methods = ("POST",))
@login_required
def create_or_update(id):
    """
    Either create a new shareholder or update existing one, depending on whether
    there is a record in DB for given primary key (path variable). Hash and
    store password only when creating new.
    """
    if request.form.get("type") == "natural":
        f = NaturalPersonForm(request.form)
        s = NaturalPerson.query.get_or_default(id, NaturalPerson())
    else:
        f = JuridicalPersonForm(request.form)
        s = JuridicalPerson.query.get_or_default(id, JuridicalPerson())

    if not f.validate():
        flash.invalid_input()
        return render_template(
            "shareholder/form.html",
            form = f,
            id = id
        )

    if id == "new":
        s.pw_hash = hashPassword(f.password.data)
        flash.create_ok("shareholder")
    else:
        flash.update_ok("shareholder")

    f.populate_obj(s)
    s.save_or_update()
    return redirect(url_for("shareholder.list"))



@bp.route("/<id>/delete", methods = ("POST",))
@login_required
def delete(id):
    """
    Delete shareholder by primary key (path variable), if found. Otherwise throw
    404. Deletes also subclass row.
    """
    if not Shareholder.query.get(id).delete_if_exists():
        abort(404)
    flash.delete_ok("shareholder")
    return redirect(url_for("shareholder.list"))
