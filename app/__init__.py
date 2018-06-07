"""
    This module creates and configures instances of the Flask app, cache, and
    database connection, for global access and use by other modules. View
    blueprints and models are registered in their respective __init__ modules.
"""

import os

from .config import (
    cache,
    config
)
from .models import (
    CustomModel,
    GetOrDefaultQuery,
    init_db
)
from .sql import get_queries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    config = config.HerokuConfig
    queries = get_queries("postgresql")
else:
    config = config.BaseConfig
    queries = get_queries()

app = Flask(__name__)
app.config.from_object(config)

cache = cache.create_cache(app)

db = SQLAlchemy(
    app,
    model_class = CustomModel,
    query_class = GetOrDefaultQuery
)
init_db(db)

from .config import auth
from .models.shareholder import Shareholder as UserClass
auth.init_auth(app, UserClass)

from .views import init_views
init_views(app)
