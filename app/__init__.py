"""
    This module creates and configures instances of the Flask app, cache, and
    database connection, for global access and use by other modules. View
    blueprints and models are registered in their respective __init__ modules.
"""

import os

from .config import config
from .config.cache import create_cache
from .models import (
    create_db,
    init_db
)
from .sql import get_statements
from flask import Flask

if os.environ.get("HEROKU"):
    config = config.HerokuConfig
else:
    config = config.BaseConfig

app = Flask(__name__)
app.config.from_object(config)

db = create_db(app)
cache = create_cache(app, db)
sql = get_statements(os.environ.get("HEROKU"))
init_db(db)

from .config import auth
auth.init_auth(app)

from .views import init_views
init_views(app)
