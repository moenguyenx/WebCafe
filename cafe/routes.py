import json
from cafe import app, menu, orders, users, finance
from flask import render_template, request, redirect, url_for
from cafe.get_time import get_date, get_current_time
from cafe.query import *
import bson.json_util as json_util
from bson import ObjectId


@app.route("/order/table/<int:table_num>", methods=['GET', 'POST'])
def order(table_num):
    if request.method == "GET":
        # Query drink list from database
        drink_list = list(menu.find())  # Converted from a cursor into a list for convenient pass
        return render_template("index.html",
                               drink_list=json.dumps(drink_list))

    if request.method == "POST":
        data = request.get_json()
        # Calculate total of bill, handle exception could happen in frontend
        total_bill = 0
        for drink in data['order']:
            total_bill += (drink['quantity'] * get_price_of_drink(drink['_id']))

        new_order = {
            "date": get_date(),
            "table": table_num,
            "order": data['order'],
            "total": total_bill,
            "status": "New"
        }
        orders.insert_one(new_order)
        return redirect(url_for('order', table_num=table_num))


@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route("/staff/dashboard", methods=['GET', 'PATCH'])
def display_staff_dashboard():
    if request.method == "GET":
        guest_orders = json_util.dumps(list(orders.find({'status': 'New'})))
        print(guest_orders)
        return render_template('staff_dashboard.html',
                               guest_orders=guest_orders,
                               name_query_function=get_name_of_drink)
    if request.method == "PATCH":
        done_order_id = ObjectId(request.json)
        orders.update_one({"_id": done_order_id},
                          {"$set": {"status": "Done"}})


@app.route("/staff/finished-orders")
def display_finished_orders():
    return render_template('staff_finished_orders.html')


@app.route("/staff/products")
def display_staff_products():
    drink_list = list(menu.find())
    return render_template('staff_products.html',
                           drink_list=json.dumps(drink_list))


@app.route("/admin/dashboard", methods=['GET', 'POST'])
def display_admin_dashboard():
    today_revenue = get_today_revenue()
    total_revenue = get_total_revenue()
    return render_template('admin_dashboard.html',
                           total_revenue="{:,.0f}".format(total_revenue),
                           today_revenue="{:,.0f}".format(today_revenue),
                           labels=json.dumps(get_day_list()),
                           data=json.dumps(get_daily_revenue_list()))


@app.route("/admin/orders")
def display_admin_orders():
    guest_orders = json_util.dumps(list(orders.find({'status': 'New'})))
    return render_template('admin_orders.html',
                           guest_orders=guest_orders)


@app.route("/admin/products", methods=['GET', 'PATCH'])
def display_admin_products():
    if request.method == "GET":
        drink_list = list(menu.find())
        return render_template('admin_products.html',
                               drink_list=json.dumps(drink_list))

    if request.method == "PATCH":
        pass


@app.route("/admin/reports")
def display_admin_reports():
    return render_template('admin_reports.html')
