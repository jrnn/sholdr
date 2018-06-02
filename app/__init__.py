"""
    This module creates and configures instances of the Flask app and database
    connection, for global access and use by other modules.

    Currently it also registers blueprints, initializes the database if needed,
    and sets up user session management with flask-login. It probably would be
    more elegant to handle these in their respective "subfolder __inits__", but
    who cares ...
"""

from .models import CustomModel
from flask import (
    Flask,
    render_template
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sholdr.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(
    app,
    model_class = CustomModel
)

from .models.shareholder import Shareholder
db.create_all()

from .views import (
    auth,
    shareholder
)
app.register_blueprint(auth.bp)
app.register_blueprint(shareholder.bp)

from flask_login import LoginManager

app.config["SECRET_KEY"] = "AllYourBaseAreBelongToUs"
app.config["BCRYPT_LOG_ROUNDS"] = 10

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "You got no business here without logging in first."
login_manager.login_message_category = "alert-danger"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return Shareholder.query.get(user_id)

@app.route("/")
def index():
    return render_template(
        "index.html",
        url = "https://github.com/jrnn/sholdr"
    )
