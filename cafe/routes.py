import json

from cafe import app, menu
from flask import render_template, request


@app.route("/", methods=["GET", "POST"])
def order():
    if request.method == "GET":
        drink_list = menu.find()
        return render_template("index.html", drink_list=json.dumps(drink_list))

    if request.method == "POST":
        pass


