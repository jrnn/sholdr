"""
    This module contains the blueprint for Shareholder management endpoints,
    spanning the standard CRUD operations. Because Shareholders come in two
    flavors (subclassing), the code is a bit bulkier than usual.
"""

from app import db
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
from sqlalchemy.orm import with_polymorphic

bp = Blueprint(
    "shareholder",
    __name__,
    url_prefix = "/shareholder"
)

@bp.route("/", methods = ("GET",))
@login_required
def list_all():
    """
    Show all shareholders on a list.

    Because shareholder has two subclasses and the data needed here is on sub-
    class level, use with_polymorphic() to make an "eager" JOIN query, so that
    needed data is all loaded up-front at once. This is to avoid a sequence of
    pointless per-entity queries (i.e. the N+1 problem).

    TO-DO : Replace ORM default with a manual, leaner query?
    """
    shareholders = db.session.query(
        with_polymorphic(
            Shareholder,
            [ JuridicalPerson, NaturalPerson ]
        )).all()

    return render_template(
        "shareholder/list.html",
        shareholders = shareholders
    )

@bp.route("/<id>", methods = ("GET",))
@login_required
def view_one(id):
    """
    Find one shareholder by primary key, then query for the correct subclass
    entity by type, and prefill corresponding form with its data.

    Whether looking at an existing shareholder or creating a new one, the same
    html template is used. The function handling the submit can tell the
    difference based on a hidden id prop passed to the form.
    """
    s = Shareholder.query.get_or_404(id)

    if s.type == "natural_person":
        s = NaturalPerson.query.get(id)
        f = NaturalPersonForm(obj = s)
    else:
        s = JuridicalPerson.query.get(id)
        f = JuridicalPersonForm(obj = s)

    return render_template(
        "shareholder/form.html",
        form = f
    )

@bp.route("/new", methods = ("GET",))
@login_required
def empty_form():
    """
    Show empty form for creating a new shareholder. Shareholder type must be
    given as query parameter so that the correct WTForm class is passed to
    Jinja.

    Whether looking at an existing shareholder or creating a new one, the same
    html template is used. The function handling the submit can tell the
    difference based on a hidden id prop passed to the form.
    """
    type = request.args.get("type")

    if type == "natural":
        f = NaturalPersonForm()
    elif type == "juridical":
        f = JuridicalPersonForm()
    else:
        flash.incorrect_type("shareholder")
        return redirect(url_for("shareholder.list_all"))

    return render_template(
        "shareholder/form.html",
        form = f
    )

@bp.route("/", methods = ("POST",))
@login_required
def create_or_update():
    """
    Either create a new shareholder or update existing one, depending on the
    inbound form's id field (process is very similar in both cases). Validate
    form data and, if errors, throw back to form view. Hash and set password
    only when creating new.
    """
    id = request.form.get("id")
    type = request.form.get("type")
    assert type == "natural" or type == "juridical"

    if type == "natural":
        f = NaturalPersonForm(request.form)
        s = NaturalPerson.query.get(id)
        if s is None:
            s = NaturalPerson()
    else:
        f = JuridicalPersonForm(request.form)
        s = JuridicalPerson.query.get(id)
        if s is None:
            s = JuridicalPerson()

    if not f.validate():
        flash.invalid_input()
        return render_template(
            "shareholder/form.html",
            form = f
        )

    del f.id  # avoid setting "new" as pk when creating new shareholder
    f.populate_obj(s)

    if id == "new":
        s.pw_hash = hashPassword(f.password.data)
        db.session.add(s)
        flash.create_ok("shareholder")
    else:
        flash.update_ok("shareholder")

    db.session.commit()
    return redirect(url_for("shareholder.list_all"))

@bp.route("/<id>/delete", methods = ("POST",))
@login_required
def delete(id):
    """
    Delete shareholder by primary key (given as path variable), if found.
    Otherwise throw 404. Also subclass row is deleted.
    """
    res = Shareholder.query.filter_by(id = id).delete()

    if res > 0:
        NaturalPerson.query.filter_by(id = id).delete()
        JuridicalPerson.query.filter_by(id = id).delete()
    else:
        abort(404)

    db.session.commit()
    flash.delete_ok("shareholder")
    return redirect(url_for("shareholder.list_all"))
