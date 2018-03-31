import os
import random
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#TODO: Fix or remove (new version swagger does not support this)
# from rest_framework_swagger.compat import strip_tags


class EmailNotification:
    """
    Class implements all email notification types
    """

    def __init__(self, user):
        self.subjects = {'new_registration': 'Registration on the website.',
                         'email_changed': 'Profile email confirmation.',
                         'new_social_account': 'Linking social account.',
                         }
        """
        :param user: is 'User' object. Person who will be emailed.
        """
        self.template_name = ''
        self.user = user
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk)),
        self.uid = self.uid[0] if type(self.uid) is tuple else self.uid

        self.token = default_token_generator.make_token(self.user),
        self.token = self.token[0] if type(self.token) is tuple else self.token

        self.site_name = os.getenv("SITE_URL", 'No site in ENV'),
        self.site_name = settings.SITE_URL #self.site_name[0] if type(self.site_name) is tuple else self.site_name
        self.mail_subject = ''
        self.context = {
            'email': self.user.email,
            'domain': settings.SITE_DOMAIN,
            'site_name': settings.SITE_DOMAIN, # NO NEED THIS, ned check everywhere and delete
            'SITE_URL': settings.SITE_URL,
            'protocol': settings.SITE_PROTOCOL,
            'uid': self.uid,
            'user': self.user,
            'token': self.token,
            'media_url': "%s%s" % (settings.SITE_URL, settings.MEDIA_URL),
        }

    def notify_superuser(self):
        """
        notification for the super admin, when:

        :return:
        """
        assert self.user.is_superuser is True, "User can not be emailed as he is not superuser"
        subject, body_txt = None, None
        self.template_name = 'email_notifications/admin/email_common'
        self.context['body_txt'] = 'TODO'

    def email_new_user_link(self):
        """
         email to new user activation link:
        :return:
        """
        # if self.user.is_superuser:
        #     assert self.user.is_superuser is True, "User can not be emailed, because it is superuser."

        self.mail_subject = self.subjects['new_registration']
        self.template_name = 'email/mail_activate_new_user'
        self.context['username'] = self.context['user'].username
        self.send_email()

    def email_add_user_social_account(self, new_user_social):
        """
         email to user link to connect his social account to db account:
        :return:
        """
        self.mail_subject = self.subjects['new_social_account']
        self.template_name = 'email/mail_activate_social_account'
        self.context['new_user_social'] = new_user_social
        self.send_email()

    def send_new_email_confirm_link(self):
        """
         send email to new user email, to confirm:
        :return:
        """
        # if self.user.is_superuser:
        #     assert self.user.is_superuser is True, "User can not be emailed, because it is superuser."

        self.mail_subject = self.subjects['email_changed']
        self.template_name = 'email/mail_email_changed_confirm'
        self.context['username'] = self.context['user'].username
        self.context['email_confirm_url'] = 'email-confirm'
        #self.user.email = self.user.email_new
        self.send_email(to_email=self.user.email_new)


    def email_password_link(self):
        """
        Method generate and send password creation link (same as forgot password option)
        to user email.
        :return:
        """
        self.mail_subject = 'Set password'
        self.template_name = 'email/email_password_recovery'
        self.context['password_url'] = 'password-recovery-redirect'
        self.send_email()

    def send_email(self, to_email=None):
        self.user.email_user(self.mail_subject, self.get_mail_text('plain'),
                             to_email=to_email, html_message=self.get_mail_text('html'))

    def get_mail_text(self, text_type='plain'):
        if text_type == 'plain':
            template_text = loader.render_to_string(self.template_name + '.txt', self.context)
        else:
            template_text = loader.render_to_string(self.template_name + '.html', self.context)

        return template_text


def generate_verify_code():
    return "".join([str(random.randint(0, 9)) for x in range(4)])

#TODO: Fix or remove
# def send_sms(msg, phone):
#     """
#     Send sms
#     :param msg:
#     :param phone:
#     """
#     client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     data = dict(body=strip_tags(msg), from_=settings.TWILIO_PHONE_NUMBER)
#
#     try:
#         client.sms.messages.create(to=str(phone), **data)
#         return True
#     except Exception as e:
#         print(_("Sms {0} to {1} not send: {2}").format(msg, phone, str(e)))
#         return False


def counters_unseen_summarize(user):
    """
    Summarize items that user does not seen. These uses in mobile app icon
    Counted data:
        - unseen post likes
        - unseen new friends
        - unseen post post comments
        - unseen messages
    :return: sum of unseen items for specific user
    """
    from friends.models import Friend
    from news.models import Like, Comment
    from user_messages.models import Dialog

    likes = Like.get_count_unseen(user)
    comments = Comment.get_count_unseen(user)
    new_friends = Friend.get_count_unseen(user)
    messages = Dialog.get_count_unread_messages(user)
    return sum([likes, comments, new_friends, messages])
