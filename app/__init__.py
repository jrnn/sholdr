"""
    This module creates instances of the Flask app and database connection, for
    global access and use by other modules.

    In an attempt to follow a kind of functional division of responsibilities,
    further configuration and initialization of these instances is spread out
    elsewhere, and carried out at call of this module.

    This is just to avoid stuffing all configuration into one bloated and messy
    file as the application grows.
"""

from flask import Flask
app = Flask(__name__)

from .sql import get_queries
queries = get_queries()

from .models import (
    create_db,
    init_db
)
db = create_db(app)
init_db(db)

from .views import init_views
init_views(app)

from .models.shareholder import Shareholder as UserClass
from .util import init_auth
init_auth(app, UserClass)
