from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.bl.utils_helper import prn
from core.serializers import ModelSerializerCore
from core.validators import validate_name
from .models import User
from django.utils.translation import ugettext_lazy as _


class UserSerializer(ModelSerializerCore):
    """
    User model serializer
    """
    email_new = serializers.EmailField(required=False,)
    username = serializers.CharField(required=False, allow_blank=True, validators=[validate_name,
                                                                                   UniqueValidator(queryset=User.objects.all(),
                                                                                                   message='A user is already registered with this username')])
    photo_clear = serializers.BooleanField(required=False, default=False)
    # date_joined = TimestampField()
    is_reported = serializers.SerializerMethodField()
    # social_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password', 'last_login')
        # fields = ("push_notification", "is_blocked", "username", "email_notification", "email_new",
        #           "token")

        extra_kwargs = {'date_joined': {'read_only': True},
                        'is_staff': {'read_only': True},
                        'is_superuser': {'read_only': True},
                        'is_active': {'read_only': True},
                        'email': {'read_only': True},
                        }
        read_only_fields = ('date_joined',)

    def validate_email_new(self, value):
        if value and User.objects.filter(email=value).first():
            raise serializers.ValidationError(
                _("A user is already registered with this email."))
        return value

    def get_is_reported(self, obj):
        is_reported = False
        user_reported_report = obj.user_reported_report.all()
        if len(user_reported_report):
            for one_report in user_reported_report:
                if 'request' in self.context and \
                                one_report.user.id == self.context['request'].user.id:
                    is_reported = True
        return is_reported

    # def get_social_info(self, obj):
    #     return obj.get_social_info()


class UserSocialSerializer(UserSerializer):
    """
    User model serializer
    """
    social_info = serializers.SerializerMethodField()

    def get_social_info(self, obj):
        return obj.get_social_info()