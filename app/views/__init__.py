"""
    This module registers all blueprints to the app instance, and defines the
    base index route.
"""

from . import (
    auth,
    shareholder
)
from flask import render_template

def init_views(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(shareholder.bp)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            url = "https://github.com/jrnn/sholdr"
        )
