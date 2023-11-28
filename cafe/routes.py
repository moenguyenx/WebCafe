import json
from cafe import app, menu
from flask import render_template, request, redirect, url_for
from cafe.forms import LoginForm


@app.route("/", methods=["GET", "POST"])
def order():
    if request.method == "GET":
        drink_list = list(menu.find())  # Converted from a cursor into a list for convenient pass
        print(drink_list)
        return render_template("index.html", drink_list=json.dumps(drink_list))

    if request.method == "POST":
        data = request.get_json()
        pass


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('display_dashboard'))
    return render_template('login.html', form=form)


@app.route("/dashboard")
def display_dashboard():
    return render_template('dashboard.html')
