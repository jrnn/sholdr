from .models import CustomModel
from flask import (
    Flask,
    render_template
)
from flask_sqlalchemy import SQLAlchemy

# create and configure instance of flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "AllYourBaseAreBelongToUs"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sholdr.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create and initialize instance of db
db = SQLAlchemy(
    app,
    model_class = CustomModel
)
from .models.shareholder import Shareholder
db.create_all()

# register blueprints
from .views import shareholder
app.register_blueprint(shareholder.bp)

# temporary bullshit just for testing purposes
@app.route("/")
def index():
    return render_template(
        "index.html",
        url = "https://github.com/jrnn/sholdr"
    )
