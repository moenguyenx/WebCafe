import json
from cafe import app, menu, orders, users, finance
from flask import render_template, request, redirect, url_for
from cafe.forms import LoginForm
from cafe.get_time import get_current_time


@app.route("/order/table/<int:table_num>", methods=['GET', 'POST'])
def order(table_num):
    if request.method == "GET":
        drink_list = list(menu.find())  # Converted from a cursor into a list for convenient pass
        print(drink_list)
        return render_template("index.html", drink_list=json.dumps(drink_list))

    if request.method == "POST":
        data = request.get_json()
        new_order = {
            "_id": get_current_time(),
            "table": table_num,
            "order": data['order'],
            "total": data['total'],
            "status": "New"
        }
        # orders.insert(new_order)
        return new_order


@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route("/staff/dashboard", methods=['GET', 'POST'])
def display_staff_dashboard():
    return render_template('staff_dashboard.html')


@app.route("/admin/dashboard", methods=['GET', 'POST'])
def display_admin_dashboard():
    return render_template('admin_dashboard.html')
