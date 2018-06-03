"""
    This module registers blueprints and error handlers to the app instance, and
    defines the base index route.
"""

from . import (
    auth,
    shareclass,
    shareholder
)
from flask import render_template

def init_views(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(shareclass.bp)
    app.register_blueprint(shareholder.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.route("/")
    def index():
        return render_template("index.html")
