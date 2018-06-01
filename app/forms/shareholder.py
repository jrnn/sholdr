from . import CustomBaseForm
from app.models.shareholder import (
    JuridicalPerson,
    Shareholder
)
from app.util.util import (
    apply_lower,
    apply_upper
)
from app.util.validation import (
    max_length,
    NinFormat,
    not_empty,
    PasswordFormat,
    RequiredIf,
    Unique
)
from wtforms import (
    PasswordField,
    StringField,
    validators
)

class ShareholderForm(CustomBaseForm):
    id = StringField(default = "new")

    email = StringField(
        "Email",
        [
            max_length(255),
            validators.Email("Invalid email format"),
            Unique(
                column = "email",
                entity = Shareholder,
                message = "Email already in use by another shareholder"
            )
        ],
        filters = [ apply_lower ],
        render_kw = { "placeholder" : "fred@flintstone.io" }
    )
    password = PasswordField(
        "Password",
        [
            RequiredIf(
                id = "new",
                validator = PasswordFormat
            )
        ],
        render_kw = { "placeholder" : "qwerty" }
    )
    street = StringField(
        "Street address",
        [
            max_length(255),
            not_empty()
        ],
        render_kw = { "placeholder" : "301 Cobblestone Way" }
    )
    street_ext = StringField(
        "Street address (optional)",
        [ max_length(255) ]
    )
    zip_code = StringField(
        "Postal code",
        [
            max_length(32),
            not_empty()
        ],
        render_kw = { "placeholder" : "70777" }
    )
    city = StringField(
        "City",
        [
            max_length(64),
            not_empty()
        ],
        render_kw = { "placeholder" : "Bedrock" }
    )
    country = StringField(
        "Country",
        [
            max_length(64),
            not_empty()
        ],
        render_kw = { "placeholder" : "United Chucks of Norris" }
    )

class NaturalPersonForm(ShareholderForm):
    type = "natural"

    first_name = StringField(
        "First name",
        [
            max_length(64),
            not_empty()
        ],
        render_kw = { "placeholder" : "Fred" }
    )
    last_name = StringField(
        "Last name",
        [
            max_length(64),
            not_empty()
        ],
        render_kw = { "placeholder" : "Flintstone" }
    )
    nin = StringField(
        "National ID / Date of birth",
        [
            max_length(11),
            not_empty(),
            NinFormat()
        ],
        filters = [ apply_upper ],
        render_kw = { "placeholder" : "070770-7071" }
    )
    nationality = StringField(
        "Nationality",
        [
            max_length(64),
            not_empty()
        ],
        render_kw = { "placeholder" : "'Murican" }
    )

class JuridicalPersonForm(ShareholderForm):
    type = "juridical"

    name = StringField(
        "Legal entity name",
        [
            max_length(128),
            not_empty()
        ],
        render_kw = { "placeholder" : "Slate Rock and Gravel Co." }
    )
    business_id = StringField(
        "Business ID",
        [
            max_length(32),
            not_empty(),
            Unique(
                column = "business_id",
                entity = JuridicalPerson,
                message = "Business ID already in use by another shareholder"
            )
        ],
        filters = [ apply_upper ],
        render_kw = { "placeholder" : "2345678-0" }
    )
    contact_person = StringField(
        "Contact person name",
        [
            max_length(128),
            not_empty()
        ],
        render_kw = { "placeholder" : "Barney Rubble" }
    )
