from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.route("/")
def home():
    return render_template("index.html")

    if request.method == "POST":
        pass


if __name__ == "__main__":
    app.run(debug=True)
