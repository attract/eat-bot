import datetime
import time

from django.conf import settings

from config.common import Common
from core.bl.utils_helper import prn


def datetime_text(datetime_obj):
    return datetime_obj.strftime(settings.DATE_FORMAT_DISPLAY + ", %I:%M %p")


def get_date_text(datetime_obj):
    if not datetime_obj:
        return ''
    if isinstance(datetime_obj, str):
        datetime_obj = datetime.datetime.strptime(datetime_obj, '%Y-%m-%d').date()
    return datetime_obj.strftime(settings.DATE_FORMAT_DISPLAY)


def get_time_text(time_obj):
    format = "%I:%M %p"
    if Common.TIME_INPUT_FORMATS:
        format = Common.TIME_INPUT_FORMATS[0]
    return time_obj.strftime(format)
