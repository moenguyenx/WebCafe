from cafe import users, menu, orders, finance, drinks
from cafe.get_time import get_date
from bson import ObjectId


def get_today_revenue():
    """
    :return: Today's Revenue
    """
    get_entry = finance.find_one({"date": get_date()})
    if get_entry is None or get_entry["revenue"] is None:
        new_doc = {
            "date": get_date(),
            "revenue": 0
        }
        finance.insert_one(new_doc)
        return 0
    else:
        return get_entry["revenue"]


def get_total_revenue():
    """
    :return: Total revenue
    """
    total_revenue = 0
    for revenue in finance.find():
        total_revenue += revenue['revenue']
    return total_revenue


def get_day_list():
    """
    :return: Days of active in Finance collection
    """
    return [date['date'] for date in finance.find()]


def get_daily_revenue_list():
    """
    :return: Daily revenue in Finance collection to display on admin dashboard
    """
    return [date['revenue'] for date in finance.find()]


def get_name_of_drink(drink_id):
    """
    :return: Name of drink from id
    :param: _id of the drink
    """
    get_entry = menu.find_one({'_id': ObjectId(drink_id)}, {'name': 1, '_id': 0})
    return get_entry['name']


def get_price_of_drink(drink_id):
    """
        :return: Price of drink from id
        :param: _id of the drink
        """
    get_entry = menu.find_one({'_id': ObjectId(drink_id)}, {'price': 1, '_id': 0})
    return get_entry['price']


def update_revenue(new_bill):
    """
    :type: Update database
    :param: New total bill add in
    """
    current_revenue = get_today_revenue()
    current_revenue += new_bill
    finance.update_one({"date": get_date()},
                       {"$set": {"revenue": current_revenue}})


def get_quantity_list():
    """
    :return: Daily revenue in Finance collection to display on admin dashboard
    """
    return [item['quantity'] for item in drinks.find().sort({'quantity': -1})]

