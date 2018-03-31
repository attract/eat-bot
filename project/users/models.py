import uuid
from urllib.error import HTTPError

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _, get_language
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from django.core.mail import send_mail
from django.utils import timezone, translation
from rest_framework.authtoken.models import Token
from sorl.thumbnail import ImageField

from core.bl.utils_helper import prn
from core.utils import generate_verify_code
from core.validators import validate_name
from django.contrib.gis.db import models as gis_models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible, force_bytes, force_text

from users.fields import JSONField
from users.manager import CustomUserManager

EMAIL_DUPLICATE_ERROR = 'This email has already been used to create an account, please use a different email.'


@python_2_unicode_compatible
class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name='Name', max_length=30, db_index=True, unique=True,
                                validators=[validate_name])
    email = models.EmailField(verbose_name='Email', unique=True,
                              error_messages={'unique': EMAIL_DUPLICATE_ERROR})
    is_staff = models.BooleanField(
        verbose_name='Staff',
        default=False,
        help_text='Designates whether the user can log into this admin site.', )
    is_active = models.BooleanField(verbose_name='Activate', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active.')
    date_joined = models.DateTimeField(verbose_name='Date creation', default=timezone.now)
    photo = ImageField('Photo', upload_to="files/profile", blank=True,
                       help_text='Profile image')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % (self.username, )
        return full_name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        abstract = True


class User(CustomAbstractUser, gis_models.Model):
    """
    Users within the Django authentication system are represented by this
    model.

    password and phone are required. Other fields are optional.
    """

    class Meta(CustomAbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('username',)
        permissions = (
            ('view_user', 'Can view'),
        )

    def __str__(self):
        if self.username:
            user_info = "%s" % self.username
            if self.email:
                user_info += " (%s)" % self.email
        else:
            user_info = "%s" % self.email
        return user_info

    @property
    def username_info(self):
        return self.__str__()

    def email_user(self, subject, message, from_email=None, to_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # do not send to admin@admin.com
        if self.email == 'admin@admin.com':
            return

        if 'html_message' not in kwargs:
            kwargs['html_message'] = message

        if not from_email:
            from_email = settings.BOSS_EMAIL

        if not to_email:
            to_email = self.email

        # print(settings.EMAIL_HOST, " ", settings.EMAIL_HOST_USER, " ",from_email)
        print('Self email=', self.email)
        send_mail(subject, message, from_email, [to_email], **kwargs)
