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
    init_db
)
from .sql import get_queries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    config = config.HerokuConfig
else:
    config = config.BaseConfig

app = Flask(__name__)
app.config.from_object(config)

cache = cache.create_cache(app)
queries = get_queries()

db = SQLAlchemy(
    app,
    model_class = CustomModel
)
init_db(db)

from .config import auth
from .models.shareholder import Shareholder as UserClass
auth.init_auth(app, UserClass)

from .views import init_views
init_views(app)
