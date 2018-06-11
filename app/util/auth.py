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

def checkPassword(password, pw_hash):
    return bcrypt.check_password_hash(pw_hash, password)

def hashPassword(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")
