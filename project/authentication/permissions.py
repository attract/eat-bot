from rest_framework import permissions
from django.utils.translation import ugettext as _

# from .models import ApiControl
from core.bl.utils_helper import prn


class UserRequestPermission(permissions.BasePermission):
    """
    Global permission check for API control.
    """
    message = _('User is blocked')

    def has_permission(self, request, view):
        return self._check(request, view)

    def has_object_permission(self, request, view, obj):
        return self._check(request, view)

    def _check(self, request, view):
        if request.user.is_authenticated:
            return not request.user.is_blocked

        return True


class IsAuthenticatedCore(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = _('User is blocked')

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_blocked
