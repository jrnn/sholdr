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
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from sqlalchemy.orm import with_polymorphic

bp = Blueprint(
    "shareholder",
    __name__,
    url_prefix = "/shareholder"
)

@bp.route("/", methods = ("GET",))
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
def view_one(id):
    """
    Find one shareholder by primary key, then query for the correct subclass
    entity by type, and prefill corresponding form with its data.

    Whether looking at an existing shareholder or creating a new one, the same
    html template is used in both cases. The function handling the submit can
    tell the difference based on a 'hidden' id prop passed to the form.
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
def empty_form():
    """
    Show empty form for creating a new shareholder. Shareholder type must be
    given as query parameter so that the correct form class is passed to Jinja.

    Whether looking at an existing shareholder or creating a new one, the same
    html template is used in both cases. The function handling the submit can
    tell the difference based on a 'hidden' id prop passed to the form.
    """
    type = request.args.get("type")

    if type == "natural":
        f = NaturalPersonForm()
    elif type == "juridical":
        f = JuridicalPersonForm()
    else:
        flash(
            "Incorrect shareholder type. Stop messing with the address bar!",
            "alert-danger"
        )
        return redirect(url_for("shareholder.list_all"))

    return render_template(
        "shareholder/form.html",
        form = f
    )

@bp.route("/", methods = ("POST",))
def create_or_update():
    """
    Either create a new shareholder or update existing one, depending on the
    inbound form's id field (process is very similar in both cases). Validate
    form data and, if errors, throw back to form view. Set password only when
    creating new.
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
        flash(
            "Check your inputs, sahib. Something's not right.",
            "alert-danger"
        )
        return render_template(
            "shareholder/form.html",
            form = f
        )

    del f.id  # avoid setting "new" as pk when creating new shareholder
    f.populate_obj(s)
    notification = "Shareholder information successfully updated!"

    if id == "new":
        s.pw_hash = "kuha_on_varaani"  ## TEMPORARY BULLSHIT
        db.session.add(s)
        notification = "New shareholder successfully created, hooray!"

    db.session.commit()
    flash(
        notification,
        "alert-success"
    )
    return redirect(url_for("shareholder.list_all"))
