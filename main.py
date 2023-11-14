from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    # with app.app_context():
    #     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafe.db"
    #     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


app = create_app()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/hihi")
def test():
    return "<h1>Testing in develop branch"


if __name__ == "__main__":
    app.run(debug=True)
