from collections import OrderedDict

import six
from django.http import Http404
from rest_framework import exceptions
from rest_framework import status
from rest_framework.compat import set_rollback
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.core.exceptions import PermissionDenied
from config.common import Common


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    custom_error = CustomError()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):

            if exc.detail is list:
                for errors in exc.detail:
                    for key, item in errors.items():
                        custom_error.add(key, item)
            else:
                for key, item in exc.detail.items():
                    custom_error.add(key, item)
        else:
            custom_error.add(Common.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY'], [exc.detail])

        set_rollback()
        return Response(custom_error.get(), status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = 'Не найден'
        custom_error.add(Common.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY'], [six.text_type(msg)])

        set_rollback()
        return Response(custom_error.get(), status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = 'Доступ запрещен'
        custom_error.add(Common.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY'], [six.text_type(msg)])

        set_rollback()
        return Response(custom_error.get(), status=status.HTTP_403_FORBIDDEN)

    return custom_error.get()


class CustomError(object):
    """
    Creates a single universal format
    {
    'errors':[
        {
          "field": "category",
          "errors": [
            "Недопустимый первичный ключ \"23\" - объект не существует."
          ]
        }
      ]
    }
    """
    def __init__(self):
        self.errors = []

    def add(self, field, errors):
        self.errors.append(self.item(field, errors))

    def item(self, field, errors):
        item = OrderedDict()
        item['field'] = field
        item['errors'] = errors
        return item

    def get(self):
        return {'errors': self.errors}
