"""
    Setup user session management with flask-login.
"""

from app import cache
from app.models.shareholder import Shareholder
from app.util.flash import error_class
from flask_login import (
    current_user,
    LoginManager,
    logout_user
)



def init_auth(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "You got no business here without logging in first."
    login_manager.login_message_category = error_class
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        return load_user_memoized(user_id)



@cache.memoize()
def load_user_memoized(user_id):
    """
    Expose LoginManager's user loader method, so that it can be passed to
    'cache.delete_memoized()' as parameter on logout.
    """
    return Shareholder.query.get(user_id)



def logout_user_memoized():
    cache.delete_memoized(
        load_user_memoized,
        current_user.id
    )
    logout_user()
