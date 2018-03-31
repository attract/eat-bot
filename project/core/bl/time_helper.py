# -*- coding: utf-8 -*-
import time
import pytz
from django.conf import settings


def timeit(method):
    # example to use: before function add line
    # @timeit
    # def func_name():
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        #print 'Function %r (%r, %r) =  %2.2f sec' % \
        #      (method.__name__, args, kw, te-ts)
        seconds = round(te - ts, 2)
        minutes = 0
        hours = 0
        if seconds > 60:
            minutes = seconds // 60
            seconds = seconds - minutes * 60
        if minutes > 60:
            hours = minutes // 60
            minutes = minutes - hours * 60
        time_string = '%ssec.' % seconds
        if minutes:
            time_string = '%sm. %ssec.' % (int(minutes), int(seconds))
        if hours:
            time_string = '%sh. %smin. %ssec' % (int(hours), int(minutes), int(seconds))
        print('Function %r, execution time = %s' % \
              (method.__name__, time_string))
        return result

    return timed


def set_timezone(datetime_value):
    tz = pytz.timezone(settings.TIME_ZONE)
    datetime_value = datetime_value.replace(tzinfo=None)
    return tz.localize(datetime_value)
