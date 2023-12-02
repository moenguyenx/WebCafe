import json
from cafe import app, menu, orders, users, finance
from flask import render_template, request, redirect, url_for
from cafe.get_time import get_date, get_current_time


@app.route("/order/table/<int:table_num>", methods=['GET', 'POST'])
def order(table_num):
    if request.method == "GET":
        drink_list = list(menu.find())  # Converted from a cursor into a list for convenient pass
        print(drink_list)
        return render_template("index.html", drink_list=json.dumps(drink_list))

    if request.method == "POST":
        data = request.get_json()
        new_order = {
            "date": get_date(),
            "table": table_num,
            "order": data['order'],
            "total": data['total'],
            "status": "New"
        }
        orders.insert_one(new_order)
        return redirect(url_for('order', table_num=table_num))


@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route("/staff/dashboard", methods=['GET', 'POST'])
async def display_staff_dashboard():
    cursor_guest_orders = await orders.find({'status': 'New'})
    guest_orders = list(cursor_guest_orders)
    return render_template('staff_dashboard.html')


@app.route("/staff/finished-orders")
def display_finished_orders():
    return render_template('staff_finished_orders.html')


@app.route("/staff/products")
def display_staff_products():
    return render_template('staff_products.html')


@app.route("/admin/dashboard", methods=['GET', 'POST'])
def display_admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route("/admin/orders")
def display_admin_orders():
    return render_template('admin_orders.html')


@app.route("/admin/products")
def display_admin_products():
    return render_template('admin_products.html')


@app.route("/admin/reports")
def display_admin_reports():
    return render_template('admin_reports.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
