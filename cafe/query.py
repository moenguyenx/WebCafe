from cafe import users, menu, orders, finance
from cafe.get_time import get_date


def get_today_revenue():
    """
    :return: Today's Revenue
    """
    get_entry = finance.find_one({"date": get_date()})
    if get_entry is None or get_entry["revenue"] is None:
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
    get_entry = menu.find_one({'_id': drink_id}, {'name': 1, '_id': 0})
    return get_entry['name']



