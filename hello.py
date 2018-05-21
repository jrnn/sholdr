from flask import (
    Flask,
    render_template
)

app = Flask(__name__)
url = "https://github.com/jrnn/sholdr"

@app.route("/")
def hello():
    return render_template(
        "index.html",
        url = url
    )

if __name__ == "__main__":
    app.run(debug = True)
