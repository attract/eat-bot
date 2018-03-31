from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BaseAuthentication

from core.bl.utils_helper import prn
from users.models import User


class AuthBackendBlock(ModelBackend):
    """Log in to Django without providing a password.

    """
    def user_can_authenticate(self, user):
        is_active = super(AuthBackendBlock, self).user_can_authenticate(user)
        is_blocked = getattr(user, 'is_blocked', None)
        if is_blocked:
            return False

        return is_active


class BlockAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise Exception('User are blocked')
