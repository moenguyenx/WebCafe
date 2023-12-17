import json
from cafe import app, menu, orders, users, finance
from flask import render_template, request, redirect, url_for, jsonify, flash
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
                               drink_list=json_util.dumps(drink_list))

    if request.method == "POST":
        data = request.json
        # Calculate total of bill, handle exception could happen in frontend
        total_bill = 0
        for drink in data['order']:
            total_bill += (drink['quantity'] * get_price_of_drink(drink['_id']))

        update_revenue(total_bill)

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
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']

        response = users.find_one({"username": input_username})
        if response is None:
            return "DEO TON TAI"
        return f'{input_username} + {input_password}'
    return render_template('login.html')


@app.route("/staff/dashboard", methods=['GET', 'PATCH'])
def display_staff_dashboard():
    if request.method == "GET":
        return render_template('staff_dashboard.html')

    if request.method == "PATCH":
        request_id = request.json['_id']
        done_order_id = ObjectId(request_id)
        orders.update_one({"_id": done_order_id},
                          {"$set": {"status": "Done"}})
        return jsonify({"message": "Successfully updated the database"})


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
                           total_revenue="{:,.0f}".format(total_revenue),
                           today_revenue="{:,.0f}".format(today_revenue),
                           labels=json.dumps(get_day_list()),
                           data=json.dumps(get_daily_revenue_list()))


@app.route("/admin/orders")
def display_admin_orders():
    guest_orders = json_util.dumps(list(orders.find({'status': 'New'})))
    return render_template('admin_orders.html',
                           guest_orders=guest_orders)


@app.route("/admin/products", methods=['GET', 'PATCH', 'DELETE', 'POST'])
def display_admin_products():
    if request.method == "GET":
        return render_template('admin_products.html')

    if request.method == "POST":
        new_drink_name = request.form['name']
        new_drink_price = request.form['price']
        new_drink_img_src = request.form['img_src']
        if menu.find_one({'name': new_drink_name.title()}) is None:
            menu.insert_one(
                {
                    'name': new_drink_name.title(),
                    'price': int(new_drink_price),
                    'img_src': new_drink_img_src
                }
            )
            return jsonify({'status': 'success', 'message': 'Successfully added new product'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Drink already existed'}), 400

    if request.method == "PATCH":
        drink_request = request.json
        drink_id = ObjectId(drink_request['_id'])
        new_price = drink_request['new_price']
        menu.update_one({'_id': drink_id},
                        {'$set': {'price': int(new_price)}})
        return jsonify({'status': 'success', 'message': 'Successfully updated price'}), 200

    if request.method == "DELETE":
        drink_request = request.json
        drink_id = ObjectId(drink_request['_id'])
        menu.delete_one({'_id': drink_id})
        return jsonify({'status': 'success', "message": "Successfully deleted item"}), 200


@app.route("/admin/reports")
def display_admin_reports():
    return render_template('admin_reports.html')


#################################################################################
# API return specific data
#################################################################################
@app.route('/get_orders_data')
def get_orders_data():
    """
    :return: New orders
    """
    new_orders = json_util.dumps(list(orders.find({'status': 'New'})))
    return jsonify(guest_orders=new_orders)


@app.route('/get_finished_orders')
def get_finished_orders():
    finished_orders = json_util.dumps(list(orders.find({'status': 'Done'})))
    return jsonify(finished_orders=finished_orders)


@app.route('/get_admin_data')
def get_admin_data():
    """
    :return: Data for Admin Dashboard
    """
    today_revenue = get_today_revenue()
    total_revenue = get_total_revenue()
    return jsonify(total_revenue="{:,.0f}".format(total_revenue),
                   today_revenue="{:,.0f}".format(today_revenue),
                   labels=json.dumps(get_day_list()),
                   data=json.dumps(get_daily_revenue_list()))


@app.route('/get_menu')
def get_menu():
    """
    :return: Whole menu
    """
    drink_list = json_util.dumps(list(menu.find()))
    return jsonify(menu=drink_list)
