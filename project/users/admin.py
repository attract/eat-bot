from django.conf import settings
from django.contrib import admin
from django.contrib.admin import TabularInline

from core.bl.utils_helper import prn
from core.templatetags.utils_tags import get_thumbnail_src
from users.forms import UserForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('email',)
    search_fields = ('email', 'username')
    list_display = ['email', 'username', 'photo_img', 'is_active', 'date_joined', ]
    fields = ('username', 'email', 'photo', 'is_active', 'date_joined', 'last_login',)
    # exclude = ('groups', 'user_permissions', 'email_new', 'password')
    readonly_fields = ('date_joined', 'last_login')
    list_filter = ()
    form = UserForm

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        return queryset

    def photo_img(self, obj):
        if obj.photo:
            return '<a href="%s" target=_blank><img src="%s"></a>' % (
                get_thumbnail_src(obj.photo, '1000', upscale=False), get_thumbnail_src(obj.photo, '70x70'))
        return ''

    photo_img.short_description = 'Photo'
    photo_img.allow_tags = True

    def social_info(self, obj):
        social_accounts = ''
        for one_social in obj.user_social.all():
            social_accounts += '%s, ' % one_social.provider

        if social_accounts:
            social_accounts = social_accounts[:-2]
        return social_accounts

    social_info.short_description = 'Social accounts'
    social_info.allow_tags = True
