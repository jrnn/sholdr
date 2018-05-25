from flask import (
    Flask,
    render_template
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "AllYourBaseAreBelongToUs"

@app.route("/")
def index():
    return render_template(
        "index.html",
        url = "https://github.com/jrnn/sholdr"
    )
