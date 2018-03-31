import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db import models
from django.db.utils import ProgrammingError

from config.common import Common


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)

        groups = None
        if 'groups' in extra_fields:
            groups = extra_fields.pop('groups')

        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        if groups:
            user.groups.add(*groups)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
