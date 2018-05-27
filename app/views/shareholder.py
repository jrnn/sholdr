from app import db
from app.forms.shareholder import (
    JuridicalPersonForm,
    NaturalPersonForm
)
from app.models.shareholder import (
    JuridicalPerson,
    NaturalPerson
)
from flask import (
    Blueprint,
    render_template,
    request
)

bp = Blueprint(
    "shareholder",
    __name__,
    url_prefix = "/shareholder"
)

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
        return "throw back to list view with error message"

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

    return "shareholder added, redirect to list view"
