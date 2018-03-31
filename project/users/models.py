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
    GCM = 'gcm'
    FCM = 'fcm'
    APNS = 'apns'
    DEVICE_TYPE = (
        (GCM, 'GCM'),
        (FCM, 'FCM'),
        (APNS, 'APNS')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name='Name', max_length=30, db_index=True, unique=True,
                                validators=[validate_name])
    email = models.EmailField(verbose_name='Email', unique=True,
                              error_messages={'unique': EMAIL_DUPLICATE_ERROR})
    email_new = models.EmailField(verbose_name='Email new', null=True, blank=True)
    is_staff = models.BooleanField(
        verbose_name='Staff',
        default=False,
        help_text='Designates whether the user can log into this admin site.', )
    is_active = models.BooleanField(verbose_name='Activate', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active.')
    is_blocked = models.BooleanField(default=False, verbose_name=_("User is blocked"),
                                     help_text='Select this instead of deleting accounts.')
    email_notification = models.BooleanField(default=True, verbose_name=_("Receive email notification"))
    push_notification = models.BooleanField(default=True, verbose_name=_("Receive push notification"))
    is_social_user = models.BooleanField(default=False, verbose_name=_("Is user registered from social network"))
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

    def get_social_info(self):
        social_info = {}
        for one_provider in dict(settings.SOCIAL_PROVIDER).keys():
            social_info[one_provider] = False

        # social_accounts = self.social_auth.all()
        social_accounts = self.user_social.filter(is_active=True).all()
        if len(social_accounts):
            for item in social_accounts:
                social_info[item.provider] = True

        return social_info

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

    def unsubscribe(self):
        """
        Method should remove user from all email sending
        :return:
        """
        raise NotImplementedError

    @classmethod
    def get_superusers(cls):
        return cls.objects.filter(is_superuser=True)

    def generate_verify_code(self):
        self.verify_code = generate_verify_code()
        self.save(update_fields=('verify_code',))

    def send_code(self):
        self.generate_verify_code()

        msg = 'Verify code: {}'.format(self.verify_code)
        # TODO: Fix or remove
        # send_sms(phone=self.phone, msg=msg)

    def get_token(self):
        """
        method help to receive User token
        :return: User token
        """
        if hasattr(self, 'token') and self.token:
            return self.token

        token, created = Token.objects.get_or_create(user=self)
        return token.key

    def logout_device(self, registration_id, for_all=False):
        if not registration_id and not for_all:
            return False
        for model in (GCMDevice, APNSDevice):
            devices = model.objects.filter(user_id=self.id)

            if registration_id:
                devices = devices.filter(registration_id=registration_id)

            devices.update(active=False)

        return True

    def create_device(self, device_type=None, registration_id=None, device_id=None):
        if device_type is None or registration_id is None:
            GCMDevice.objects.filter(user=self).delete()
            APNSDevice.objects.filter(user=self).delete()
        else:
            device_data = {
                'registration_id': registration_id,
                'device_id': device_id,
                'user': self
            }
            if device_type == 'gcm':
                APNSDevice.objects.filter(user=self).delete()
                GCMDevice.objects.filter(Q(user=self) | Q(registration_id=registration_id)).delete()
                GCMDevice(**device_data).save()

            elif device_type == 'fcm':
                device_data['application_id'] = 'fcm'
                device_data['cloud_message_type'] = 'FCM'
                APNSDevice.objects.filter(user=self).delete()
                GCMDevice.objects.filter(Q(user=self) | Q(registration_id=registration_id)).delete()
                GCMDevice(**device_data).save()

            elif device_type == 'apns':
                applications = ['ios_live', 'ios_sandbox']

                GCMDevice.objects.filter(user=self).delete()
                APNSDevice.objects.filter(Q(user=self) | Q(registration_id=registration_id)).delete()

                for application_id in applications:
                    device_data['application_id'] = application_id
                    try:
                        APNSDevice(**device_data).save()
                    except Exception as ex:
                        print(ex)

                # GCMDevice.objects.filter(user=self).delete()
                # old_devices = APNSDevice.objects.filter(user=self)
                # device = APNSDevice.objects.filter(registration_id=registration_id).first()
                # if device:
                #     apns_serializer = APNSDeviceSerializer(instance=device, data=device_data)
                #     old_devices = old_devices.exclude(pk=device.pk)
                # else:
                #     apns_serializer = APNSDeviceSerializer(data=device_data)
                #
                # apns_serializer.is_valid(raise_exception=True)
                #
                # old_devices.delete()
                #
                # apns_serializer.save(user=self)

    def send_push_notification(self, msg, type_, **kwargs):
        User.bulk_send_push_notification([self], msg, type_, **kwargs)

        # to call example
        # push = settings.PUSH_NOTIFICATIONS_MESSAGES['PHOTO_WINS_COMPETITION']
        # kwargs = {'extra': {}, 'title': push['title']}
        # user.send_push_notification(msg=push['msg'], type_=push['type'], **kwargs)

    @staticmethod
    def bulk_send_push_notification(users, msg, type_, **kwargs):

        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        language = get_language()
        kwargs['extra']['type'] = type_
        prn(kwargs['extra'])
        users_send = []
        for model in (GCMDevice, APNSDevice):
            for user in users:

                # If user is login in mobile
                # if user.is_mobile_login is False:
                #     continue

                # If user set off push notifications
                if user.push_notification is False:
                    continue

                # translation.activate(user.language)
                count = user.get_badge()

                if model == APNSDevice:

                    for application_id in ['ios_live', 'ios_sandbox']:
                        try:
                            model.objects.filter(user_id=user.id, application_id=application_id) \
                                .send_message(str(msg),
                                              sound="default",
                                              content_available=1,
                                              badge=count, **kwargs)
                        except Exception as e:
                            print(_("Push notification to {0} not send on {1}. Error: {2}").format(user, model, str(e)))

                elif model == GCMDevice:

                    for application_id in ['android_sandbox', 'android_live', 'fcm']:
                        gcm_push_devices = model.objects.filter(user_id=user.id, application_id=application_id)
                        try:
                            gcm_push_devices.send_message(str(msg), sound="default", content_available=True, **kwargs)
                            for one_gcm_push_device in gcm_push_devices: 
                                prn(one_gcm_push_device.registration_id)
                        except Exception as e:
                            print(_("Push notification to {0} not send on {1}. Error: {2}").format(user, model, str(e)))

                users_send.append(user)

        translation.activate(language)
        return users_send

    def get_badge(self):
        """
        Method uses for generating values for 'badge' field of IOS devices
        :return:
        """
        return 0

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


class UserSocial(models.Model):
    user = models.ForeignKey(User, related_name='user_social',
                             on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = JSONField()
    is_active = models.BooleanField(default=False)
    token = models.TextField(max_length=1000, default='')
    token_secret = models.TextField(max_length=1000, default='')

    def __str__(self):
        return str(self.user)

    def get_app_secret(self):
        app_secret = ''

        if self.provider == settings.FACEBOOK_PROVIDER:
            app_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        elif self.provider == settings.TWITTER_PROVIDER:
            app_secret = settings.SOCIAL_AUTH_TWITTER_SECRET
        elif self.provider == settings.PINTEREST_PROVIDER:
            app_secret = settings.SOCIAL_AUTH_PINTEREST_SECRET

        return app_secret

    def set_token(self, token, token_secret=''):
        app_secret = self.get_app_secret()
        self.token = urlsafe_base64_encode(force_bytes(app_secret+token))

        if token_secret:
            self.token_secret = urlsafe_base64_encode(force_bytes(app_secret + token_secret))

    def get_token(self, need_secret=False):
        app_secret = self.get_app_secret()
        if need_secret:
            # get token_secret
            return force_text(urlsafe_base64_decode(self.token_secret)).replace(app_secret, '')
        else:
            # get main token
            return force_text(urlsafe_base64_decode(self.token)).replace(app_secret, '')

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        # app_label = "social_django"
        # db_table = 'social_auth_usersocialauth'
