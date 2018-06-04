"""
    This module handles auth/security-related app configuration, namely, the
    setup of flask-login for user session management; and cache configuration.
    Cache timeout is quite long (15 minutes), but this should not be a problem
    because the entire cache is flushed at every non-read DB operation.
"""

from .flash import error_class
from app.util.util import get_uuid
from flask_caching import Cache
from flask_login import LoginManager

def init_auth(app, UserClass, cache):
    app.config["SECRET_KEY"] = get_uuid()
    app.config["BCRYPT_LOG_ROUNDS"] = 10

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

def init_cache(app):
    cache = Cache(config = {
        "CACHE_DEFAULT_TIMEOUT" : 900,
        "CACHE_TYPE" : "simple"
    })
    cache.init_app(app)

    with app.app_context():
        cache.clear()
    return cache
