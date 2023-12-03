import json
from cafe import app, menu, orders, users, finance
from flask import render_template, request, redirect, url_for
from cafe.get_time import get_date, get_current_time
from cafe.query import get_today_revenue, get_total_revenue, get_daily_revenue_list, get_day_list, get_name_of_drink
import bson.json_util as json_util


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
def display_staff_dashboard():
    guest_orders = json_util.dumps(list(orders.find({'status': 'New'})))
    print(guest_orders)
    return render_template('staff_dashboard.html',
                           guest_orders=guest_orders,
                           name_query_function=get_name_of_drink)


@app.route("/staff/finished-orders")
def display_finished_orders():
    return render_template('staff_finished_orders.html')


@app.route("/staff/products")
def display_staff_products():
    return render_template('staff_products.html')


@app.route("/admin/dashboard", methods=['GET', 'POST'])
def display_admin_dashboard():
    today_revenue = get_today_revenue()
    total_revenue = get_total_revenue()
    return render_template('admin_dashboard.html',
                           total_revenue=total_revenue,
                           today_revenue=today_revenue,
                           labels=json.dumps(get_day_list()),
                           data=json.dumps(get_daily_revenue_list()))


@app.route("/admin/orders")
def display_admin_orders():
    return render_template('admin_orders.html')


@app.route("/admin/products")
def display_admin_products():
    return render_template('admin_products.html')


@app.route("/admin/reports")
def display_admin_reports():
    return render_template('admin_reports.html')
