"""
    This module creates and configures instances of the Flask app, cache, and
    database connection, for global access and use by other modules. View
    blueprints and models are registered in their respective __init__ modules.
"""

from .config.cache import create_cache
from .config.config import get_config
from .models import (
    create_db,
    init_db
)
from .sql import get_statements
from flask import Flask

app = Flask(__name__)
app.config.from_object(get_config())

db = create_db(app)
cache = create_cache(app, db)
sql = get_statements()
init_db(db)

from .config.auth import init_auth
from .views import init_views
init_auth(app)
init_views(app)
