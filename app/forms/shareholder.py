"""
    This module contains the WTForm classes that handle Shareholder forms: a
    common base for shared fields, and one subform for each subclass. A tweaked
    base class that trims surrounding whitespace from all fields is applied.

    Shareholders are the heaviest entity in the app (in terms of number of
    attributes), so the form classes are quite hefty too, with layers of
    validation and customization.
"""

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
    MaxLength,
    NinFormat,
    NotEmpty,
    PasswordFormat,
    RequiredIf,
    Unique
)
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    validators
)



class ShareholderForm(CustomBaseForm):
    id = StringField(default = "new")
    email = StringField(
        filters = [ apply_lower ],
        label = "Email",
        render_kw = { "placeholder" : "fred@flintstone.io" },
        validators = [
            MaxLength(255),
            validators.Email("Invalid email format"),
            Unique(
                column = "email",
                entity = Shareholder,
                message = "Email already in use by another shareholder"
            )
        ]
    )
    password = PasswordField(
        label = "Password",
        render_kw = { "placeholder" : "qwerty" },
        validators = [
            RequiredIf(
                id = "new",
                validator = PasswordFormat
            )
        ]
    )
    street = StringField(
        label = "Street address",
        render_kw = { "placeholder" : "301 Cobblestone Way" },
        validators = [
            MaxLength(255),
            NotEmpty()
        ]
    )
    street_ext = StringField(
        label = "Street address (optional)",
        validators = [ MaxLength(255) ]
    )
    zip_code = StringField(
        label = "Postal code",
        render_kw = { "placeholder" : "70777" },
        validators = [
            MaxLength(32),
            NotEmpty()
        ]
    )
    city = StringField(
        label = "City",
        render_kw = { "placeholder" : "Bedrock" },
        validators = [
            MaxLength(64),
            NotEmpty()
        ]
    )
    country = StringField(
        label = "Country",
        render_kw = { "placeholder" : "United Chucks of Norris" },
        validators = [
            MaxLength(64),
            NotEmpty()
        ]
    )
    has_access = BooleanField(
        default = True,
        label = "Access rights (can login to sholdr)"
    )
    is_admin = BooleanField(
        default = False,
        label = "Administrator (god-mode)"
    )



class NaturalPersonForm(ShareholderForm):
    type = "natural"
    first_name = StringField(
        label = "First name",
        render_kw = { "placeholder" : "Fred" },
        validators = [
            MaxLength(64),
            NotEmpty()
        ]
    )
    last_name = StringField(
        label = "Last name",
        render_kw = { "placeholder" : "Flintstone" },
        validators = [
            MaxLength(64),
            NotEmpty()
        ]
    )
    nin = StringField(
        filters = [ apply_upper ],
        label = "National ID / Date of birth",
        render_kw = { "placeholder" : "070770-7071" },
        validators = [ NinFormat() ]
    )
    nationality = StringField(
        label = "Nationality",
        render_kw = { "placeholder" : "'Murican" },
        validators = [
            MaxLength(64),
            NotEmpty()
        ]
    )



class JuridicalPersonForm(ShareholderForm):
    type = "juridical"
    name = StringField(
        label = "Legal entity name",
        render_kw = { "placeholder" : "Slate Rock and Gravel Co." },
        validators = [
            MaxLength(128),
            NotEmpty()
        ]
    )
    business_id = StringField(
        filters = [ apply_upper ],
        label = "Business ID",
        render_kw = { "placeholder" : "2345678-0" },
        validators = [
            MaxLength(32),
            NotEmpty(),
            Unique(
                column = "business_id",
                entity = JuridicalPerson,
                message = "Business ID already in use by another shareholder"
            )
        ]
    )
    contact_person = StringField(
        label = "Contact person name",
        render_kw = { "placeholder" : "Barney Rubble" },
        validators = [
            MaxLength(128),
            NotEmpty()
        ]
    )
