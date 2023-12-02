from cafe import users, menu, orders, finance
from cafe.get_time import get_date


def get_today_revenue():
    """
    :return: Today's Revenue
    """
    return finance.find_one({"date": get_date()})['revenue']


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



