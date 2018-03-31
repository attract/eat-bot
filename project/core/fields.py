import re

import datetime
from phonenumber_field.phonenumber import to_python
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import serializers
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError


def serializer_custom_validate_international_phonenumber(value):

    value = re.sub('[ -]', '', value)
    if value.startswith('+') is False:
        if len(value) == 10:
            value = "+1%s" % value
        elif len(value) == 11:
            value = "+%s" % value

    phone_number = to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(_('The phone number entered is not valid.'))


class SerializerPhoneNumberField(serializers.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid phone number.'),
    }
    default_validators = [serializer_custom_validate_international_phonenumber]

    def to_python(self, value):
        phone_number = to_python(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return phone_number


class TimestampField(serializers.DateTimeField):
    def to_representation(self, value):
        if not value:
            return None

        output_format = '%s'
        return int(value.strftime(output_format))

