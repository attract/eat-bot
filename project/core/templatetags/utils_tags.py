from collections import OrderedDict

from django import template
from django.conf import settings
from django.utils.numberformat import format as format_number
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
from sorl.thumbnail import get_thumbnail

from core.bl.utils_helper import prn

ADMIN_CHANGE_LIST_ROWS_CLASS = {
    'row_with_error': 'error',
    'row_with_success': 'success',
    'row_with_warning': 'warning',
    'row_with_info': 'info',
}

register = template.Library()


def get_ctx(context):
    ''' submit buttons context change '''
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another',
                                                 ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue',
                                              ctx['show_save_and_continue']),
        'show_save': context.get('show_save',
                                 ctx['show_save']),
        'show_delete_link': context.get('show_delete_link', ctx['show_delete_link'])
    })
    return ctx


@register.simple_tag
def multiply_values(val1=0, val2=0, floatformat=2):
    floatformat = '%.' + str(floatformat) + 'f'
    result = floatformat % (val1 * val2)

    return result


# FILTERS STARTS HERE
@register.filter
def print_value(value):
    print('value_type = ')
    prn(value)
    return type(value)


@register.filter
def check_row_class(values):
    if isinstance(values, list):
        for item in values:
            for class_search, row_class in ADMIN_CHANGE_LIST_ROWS_CLASS.items():
                if class_search in item:
                    return ' %s' % row_class
    elif isinstance(values, OrderedDict) or isinstance(values, dict):
        for field_name, item in values.items():
            item_str = "%s" % item
            for class_search, row_class in ADMIN_CHANGE_LIST_ROWS_CLASS.items():
                if class_search in item_str:
                    return ' %s' % row_class
    return ''


@register.filter
def sexy_money(value, n=3, sep=".", fil=" "):
    tail = 0
    stack = []
    counter = n
    value = str(value)
    head = value

    if sep in value:
        head, tail = value.split(sep)

    while len(head) >= counter:
        stack.append(head[-counter:])
        head = head[:len(head)-counter]

    stack.append(head)
    stack.reverse()
    try:
        return "".join([fil.join(stack).lstrip(fil),
                sep if int(tail) > 0 else '',
                tail if int(tail) > 0 else ''])
    except:
        return 0


@register.filter
def replace_str(value, param):
    # example to call filter
    # {% variable_string|replace_str:",|." %}
    if param is None:
        return False
    src, dst = param.split('|', 1)
    return value.replace(src, dst)


@register.filter
def keyvalue(dict, key):
    if key in dict:
        return dict[key]
    else:
        return False


@register.filter
def max_length(value, max_length):
    return (value[:max_length-2] + '..') if len(value) > max_length else value


@register.filter(is_safe=True)
def float_with_dot(value, decimal_pos=2):
    return format_number(value, '.', decimal_pos)


@register.filter
def is_svg_image(image_src):
    if u'</svg>' in image_src:
        return True
    else:
        return False


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def has_perms_users_groups(request, users_groups):

    has_perms = True
    if users_groups:

        has_perms = False
        for group in users_groups:
            if hasattr(request.user, group):
                if getattr(request.user, group):
                    has_perms = True

    return has_perms


@register.simple_tag
def check_perms_model_users_groups(request, users_groups, models):
    clean_models = []
    for model in models:
        is_model_show = True
        if 'users_groups' in model:
            is_model_show = has_perms_users_groups(request, model['users_groups'])
        if is_model_show:
            clean_models.append(model)
    return clean_models


@register.simple_tag
def get_thumbnail_src(img_field, size, **kwargs):

    try:
        thumbnail_url = get_thumbnail(img_field, size, **kwargs).url
    except (IOError, ) as error:
        print(error)
        return '#'

    return thumbnail_url


@register.simple_tag
def google_calendar_create_event(schedule_truck):
    """
    dates:
        Example: dates=20090621T063000Z/20090621T080000Z
               (i.e. an event on 21 June 2009 from 7.30am to 9.0am
                British Summer Time (=GMT+1)).
        Format: dates=YYYYMMDDToHHMMSSZ/YYYYMMDDToHHMMSSZ
               This required parameter gives the start and end dates and times
               (in Greenwich Mean Time) for the event.

    :param schedule_truck:
    :return:
    """
    api = "http://www.google.com/calendar/event"

    # print(schedule_truck)
    name = schedule_truck['schedule__event__name']
    dates = "%sT%s/%sT%s" % (schedule_truck['schedule__date'].strftime('%Y%m%d'),
                        schedule_truck['schedule__event__time_start'].strftime('%H%M00'),
                        schedule_truck['schedule__date'].strftime('%Y%m%d'),
                        schedule_truck['schedule__event__time_end'].strftime('%H%M00'),)

    details = schedule_truck['schedule__event__location']
    location = schedule_truck['schedule__event__location']

    return "{api}?action=TEMPLATE&" \
           "text={name}&" \
           "dates={dates}&" \
           "details={details}&" \
           "location={location}&" \
           "trp=false&sprop=&sprop=name:".format(
                                                api=api,
                                                name=name,
                                                dates=dates,
                                                details=details,
                                                location=location)
