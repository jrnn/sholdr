"""
    Setup user session management with flask-login.
"""

from app import cache
from app.util.flash import error_class
from app.util.util import get_uuid
from flask_login import LoginManager

def init_auth(app, UserClass):
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "You got no business here without logging in first."
    login_manager.login_message_category = error_class
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    @cache.memoize()
    def load_user(user_id):
        return UserClass.query.get(user_id)
