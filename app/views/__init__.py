"""
    This module registers blueprints and error handlers to the app instance, and
    defines the base index route.
"""

from . import (
    auth,
    certificate,
    share,
    shareclass,
    shareholder,
    transaction
)
from flask import (
    redirect,
    render_template,
    url_for
)
from flask_login import (
    current_user,
    login_required
)



def init_views(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(certificate.bp)
    app.register_blueprint(share.bp)
    app.register_blueprint(shareclass.bp)
    app.register_blueprint(shareholder.bp)
    app.register_blueprint(transaction.bp)

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

    @app.route("/")
    @login_required
    def my_page():
        return redirect(url_for(
            "shareholder.details",
            id = current_user.get_id()
        ))
