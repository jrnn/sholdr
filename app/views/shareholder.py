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
    Because shareholder has two subclasses and the data needed here is in those
    subclasses, use with_polymorphic() to make an "eager" JOIN query, so that
    needed data is all loaded up-front at once. This is to avoid a sequence of
    pointless per-entity queries afterwards (i.e. the N+1 problem).

    TO-DO : Replace ORM default with a manual, lightweight query?
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
    return "render shareholder/form.html with prefilled form depending on type"

@bp.route("/new", methods = ("GET",))
def form():
    """
    Select form depending on shareholder type, which is given as query param.
    """
    type = request.args.get("type")

    if type == "natural":
        return render_template(
            "shareholder/form.html",
            form = NaturalPersonForm()
        )
    elif type == "juridical":
        return render_template(
            "shareholder/form.html",
            form = JuridicalPersonForm()
        )
    else:
        ## TO-DO : error message
        return redirect(url_for("shareholder.list_all"))

@bp.route("/", methods = ("POST",))
def create():
    type = request.form.get("type")
    assert type == "natural" or type == "juridical"

    if type == "natural":
        f = NaturalPersonForm(request.form)
        s = NaturalPerson()

        s.first_name = f.first_name.data.strip()
        s.last_name = f.last_name.data.strip()
        s.nin = f.nin.data.strip()
        s.nationality = f.nationality.data.strip()

    else:
        f = JuridicalPersonForm(request.form)
        s = JuridicalPerson()

        s.name = f.name.data.strip()
        s.business_id = f.business_id.data.strip()
        s.contact_person = f.contact_person.data.strip()

    if not f.validate():
        # TO-DO : error message
        return render_template(
            "shareholder/form.html",
            form = f
        )

    s.email = f.email.data.strip()
    s.pw_hash = f.password.data.strip()
    s.street = f.street.data.strip()
    s.street_ext = f.street_ext.data.strip()
    s.zip_code = f.zip_code.data.strip()
    s.city = f.city.data.strip()
    s.country = f.country.data.strip()

    db.session().add(s)
    db.session().commit()

    ## TO-DO : success message
    return redirect(url_for("shareholder.list_all"))
