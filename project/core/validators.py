import re
import string

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.utils import timezone

from core.bl.utils_helper import prn

MAX_FILE_SIZE = 5000000


def non_zero_validation(value):
    if value <= 0:
        raise ValidationError('Value should not be zero or less')


def validate_address(value):
    #if len(value.split(',')) < 4:
    if not value:
        raise ValidationError('Address should be more precise')


def validate_file_size(file):
    if file.size > MAX_FILE_SIZE:
        raise serializers.ValidationError('Видео должен быть не более 5Мб')


def validate_date(date):
    """
    validate date to be now, present or future (not past)
    :param date: entered to field date
    :return:
    """
    if timezone.now().date() > date:
        raise ValidationError('Date should be present or future')


def validate_name(value):
    """
    validate name or other value for non readable symbols
    if value is empty, than function don't check
    :param value: entered to field date
    :return:
    """
    match_rule = '[A-Za-z0-9- .,&`\'"!?$%*()_]+'
    if value and not re.match(r'^%s$' % match_rule, value):
        not_allowed_symbols = re.sub(r'%s' % match_rule, '', value)
        unique_symbols = ''
        for item in not_allowed_symbols:
            if item not in unique_symbols:
                unique_symbols += item
        raise ValidationError('''Enter a valid value. You use an invalid character: %s'''
                              % unique_symbols)
