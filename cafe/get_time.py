from datetime import datetime


def get_date():
    current = datetime.now()
    day = current.strftime("%d")
    month = current.strftime("%m")
    year = current.strftime("%Y")

    date = f"{day}-{month}-{year}"

    return f"{date}"


def get_current_time():
    current = datetime.now()
    hour = current.strftime("%H")  # 0-23h
    minute = current.strftime("%M")

    current_time = f"{hour}{minute}"

    return f"{current_time}"
