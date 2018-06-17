"""
    This module houses authentication- and security-related operations: namely,
    setup of user session management with flask-login, and password hashing with
    flask-bcrypt.
"""

from app import (
    app,
    cache
)
from app.models.shareholder import Shareholder
from flask_bcrypt import Bcrypt
from flask_login import (
    current_user,
    LoginManager,
    logout_user
)
from functools import wraps



login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

login_manager.login_view = "auth.login"
login_manager.login_message = None
login_manager.session_protection = "strong"

@login_manager.user_loader
@cache.memoize()
def load_user(user_id):
    return Shareholder.query.get(user_id)

def logout_user_memoized():
    cache.delete_memoized(
        load_user,
        current_user.id
    )
    logout_user()

def login_required(role = None):
    """
    Tweaked @login_required decorator that should otherwise work similarly as
    the flask-login standard, but the keyword "ADMIN" can be passed to delimit
    certain views to administrators only. Access rights in the app are very
    simple (only basic vs. admin distinction).
    """
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.get_id():
                return login_manager.unauthorized()

            if not (current_user.is_authenticated() and current_user.is_active()):
                return login_manager.unauthorized()

            if role == "ADMIN" and not current_user.is_admin:
                return login_manager.unauthorized()

            return f(*args, **kwargs)
        return decorated_view
    return wrapper

def checkPassword(password, pw_hash):
    return bcrypt.check_password_hash(pw_hash, password)

def hashPassword(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")
