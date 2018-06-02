"""
    This module handles auth/security-related app configuration, namely, the
    setup of flask-login for user session management.
"""

from .flash import error_class
from flask_login import LoginManager
from os import urandom

def init_auth(app, UserClass):
    app.config["SECRET_KEY"] = urandom(32)
    app.config["BCRYPT_LOG_ROUNDS"] = 10

    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "You got no business here without logging in first."
    login_manager.login_message_category = error_class
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        return UserClass.query.get(user_id)
