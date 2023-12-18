import json
from cafe import app, menu, orders, users, finance, bcrypt
from flask import render_template, request, redirect, url_for, jsonify, flash
from cafe.get_time import get_date, get_current_time
from cafe.query import *
import bson.json_util as json_util
from bson import ObjectId


#################################################################################
# Order page for customer
#################################################################################
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
        return jsonify({'status': 'success', 'message': 'Successfully placed your order'}), 200


#################################################################################
# Login page
#################################################################################
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']

        user = users.find_one({"username": input_username})

        if user is None:
            flash('User not found.', 'error')
            return redirect(url_for('login'))

        stored_password = user['password']
        if bcrypt.check_password_hash(stored_password, input_password) and user['username'] == 'admin':
            # login successful as Admin
            flash('Login successful as admin!', 'success')
            return redirect(url_for('display_admin_dashboard'))
        elif bcrypt.check_password_hash(stored_password, input_password) and user['username'] == 'staff':
            # login successful as Staff
            flash('Login successful as staff!', 'success')
            return redirect(url_for('display_staff_dashboard'))
        else:
            # Password do not match
            flash('Incorrect password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


#################################################################################
# Display staff dashboard, contains new orders
#################################################################################
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


#################################################################################
# Display staff finished orders
#################################################################################
@app.route("/staff/finished-orders")
def display_finished_orders():
    return render_template('staff_finished_orders.html')


#################################################################################
# Products page for staff
#################################################################################
@app.route("/staff/products")
def display_staff_products():
    return render_template('staff_products.html')


#################################################################################
# Display admin dashboard
#################################################################################
@app.route("/admin/dashboard")
def display_admin_dashboard():
    return render_template('admin_dashboard.html')


#################################################################################
# Display unfinished order for admin
#################################################################################
@app.route("/admin/orders")
def display_admin_orders():
    return render_template('admin_orders.html')


#################################################################################
# Products page for admin to perform CRUD operation on the menu
#################################################################################
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


#################################################################################
# Unfinished function :)))))
#################################################################################
@app.route("/admin/reports")
def display_admin_reports():
    return render_template('admin_reports.html')


#################################################################################
# API return specific data in JSON
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
    """
    :return: Finished orders
    """
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


#################################################################################
# Secrete function to create more user 
#################################################################################
def create_user(username, password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if the username already exists
    if users.find_one({"username": username}):
        return jsonify({'status': 'error', 'message': 'Username already exists.'}), 400

    # Insert the new user into the database
    user_data = {"username": username, "password": hashed_password}
    users.insert_one(user_data)

    return jsonify({'status': 'success', 'message': 'User created successfully.'}), 201


@app.route("/create_user", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        return create_user(input_username, input_password)
    if request.method == 'GET':
        return render_template('createUser.html')
