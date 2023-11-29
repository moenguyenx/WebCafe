from datetime import datetime


def get_current_time():
    current = datetime.now()
    day = current.strftime("%d")
    month = current.strftime("%m")
    year = current.strftime("%y")
    hour = current.strftime("%H")  # 0-23h
    minute = current.strftime("%M")

    date = f"{day}{month}{year}"
    current_time = f"{hour}{minute}"

    return f"{current_time}{date}"

# print(get_current_time())
