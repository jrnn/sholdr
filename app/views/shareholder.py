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
    Because shareholder has two subclasses and the data needed here is on sub-
    class level, use with_polymorphic() to make an "eager" JOIN query, so that
    needed data is all loaded up-front at once. This is to avoid a sequence of
    pointless per-entity queries (i.e. the N+1 problem).

    TO-DO : Replace ORM default with a manual, more lightweight query?
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
    entity by type, and prefill corresponding form with its data. The same form
    template is used as when creating new shareholders, but the form action on
    submit points at the 'update' route, singled by id.
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
        form = f,
        form_action = url_for("shareholder.create") + id
    )

@bp.route("/new", methods = ("GET",))
def form():
    """
    Shareholder type must be given as query parameter, based on which the
    correct form is passed to Jinja. Form action on submit is set to point at
    'create' route.
    """
    type = request.args.get("type")

    if type == "natural":
        f = NaturalPersonForm()
    elif type == "juridical":
        f = JuridicalPersonForm()
    else:
        ## TO-DO : error message
        return redirect(url_for("shareholder.list_all"))

    return render_template(
        "shareholder/form.html",
        form = f,
        form_action = url_for("shareholder.create")
    )

@bp.route("/", methods = ("POST",))
def create():
    """
    Convert html form into corresponding WTForm and run validation. If errors,
    throw back to form view. Otherwise populate a new shareholder object with
    form data and save into db.
    """
    type = request.form.get("type")
    assert type == "natural" or type == "juridical"

    if type == "natural":
        f = NaturalPersonForm(request.form)
        s = NaturalPerson()
    else:
        f = JuridicalPersonForm(request.form)
        s = JuridicalPerson()

    if not f.validate():
        # TO-DO : error message
        return render_template(
            "shareholder/form.html",
            form = f,
            form_action = url_for("shareholder.create")
        )

    f.populate_obj(s)
    s.pw_hash = "kuha_on_varaani"  ## TEMPORARY BULLSHIT

    db.session.add(s)
    db.session.commit()

    ## TO-DO : success message
    return redirect(url_for("shareholder.list_all"))

@bp.route("/<id>", methods = ("POST",))
def update(id):
    """
    Very similar to create() above, but instead of adding new shareholder, fetch
    existing one from db, overwrite it with form data, and save changes.

    TO-DO : maybe create() and update() should be integrated into one method?
    """
    type = request.form.get("type")
    assert type == "natural" or type == "juridical"

    if type == "natural":
        s = NaturalPerson.query.get_or_404(id)
        f = NaturalPersonForm(request.form)
    else:
        s = JuridicalPerson.query.get_or_404(id)
        f = JuridicalPersonForm(request.form)

    if not f.validate():
        # TO-DO : error message
        return render_template(
            "shareholder/form.html",
            form = f,
            form_action = url_for("shareholder.create") + id
        )

    f.populate_obj(s)
    db.session.commit()

    ## TO-DO : success message
    return redirect(url_for("shareholder.list_all"))
