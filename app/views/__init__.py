"""
    This module registers blueprints and error handlers to the app instance, and
    defines the base index route.
"""

from . import (
    auth,
    certificate,
    share,
    shareclass,
    shareholder
)
from flask import render_template



def init_views(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(certificate.bp)
    app.register_blueprint(share.bp)
    app.register_blueprint(shareclass.bp)
    app.register_blueprint(shareholder.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        print(e)
        return render_template("500.html"), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        print(e)
        return render_template("500.html"), 500

    app.add_url_rule("/", "shareholder.list")
