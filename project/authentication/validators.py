from django.conf import settings
from django.contrib.auth import password_validation
from django.core import exceptions
from rest_framework import serializers

from core.bl.utils_helper import prn
from users.models import User


class ValidatePasswordMixin(object):
    def validate_password(self, value):
        """
        Validation of password
        """
        password = value

        min_length = settings.AUTH_PASSWORD_VALIDATORS[0]['OPTIONS']['min_length']
        if len(password) < min_length:
            # MIN LENGTH CUSTOM ERROR MESSAGE
            raise serializers.ValidationError({'password':
                                                   list(['Your password must be at least %s characters' % min_length])})
        try:
            password_validation.validate_password(password=password, user=User)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return value
