from app import db
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
    Slightly different forms depending on shareholder type.
    """
    type = request.args.get("type")
    if type == "natural":
        return render_template("shareholder/form_natural.html")
    elif type == "juridical":
        return render_template("shareholder/form_juridical.html")
    else:
        return "throw back to list view with error message"

@bp.route("/", methods = ("POST",))
def create():
    """
    Pick subclass and fill in data depending on type.
    """
    f = request.form
    type = f.get("type")
    assert type == "natural" or type == "juridical"

    if type == "natural":
        s = NaturalPerson()

        s.first_name = f.get("first_name")
        s.last_name = f.get("last_name")
        s.nin = f.get("nin")
        s.nationality = f.get("nationality")

    else:
        s = JuridicalPerson()

        s.name = f.get("name")
        s.business_id = f.get("business_id")
        s.contact_person = f.get("contact_person")

    s.email = f.get("email")
    s.pw_hash = f.get("password")
    s.street = f.get("street")
    s.street_ext = f.get("street_ext")
    s.zip_code = f.get("zip_code")
    s.city = f.get("city")
    s.country = f.get("country")

    db.session().add(s)
    db.session().commit()

    return "shareholder added, redirect to list view"
