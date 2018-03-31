from datetime import timedelta, date

from core.bl.utils_helper import prn


def get_week_start_end():
    today = date.today()
    date_start = today - timedelta(days=today.weekday())
    date_end = date_start + timedelta(days=6)

    return date_start, date_end
