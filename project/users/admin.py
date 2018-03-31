from django.conf import settings
from django.contrib import admin
from django.contrib.admin import TabularInline

from core.bl.utils_helper import prn
from core.templatetags.utils_tags import get_thumbnail_src
from users.forms import UserForm
from .models import User, UserSocial


class UserSocialInlineAdmin(TabularInline):
    model = UserSocial
    fields = ['provider', 'uid', 'is_active']
    readonly_fields = fields
    extra = 0

    # def building_link(self, obj):
    #     output = ''
    #     buildings = Building.objects.filter(owner_id=obj.id)
    #     if not buildings.count():
    #         output = 'not found'
    #     for item in buildings:
    #         output += '<a href="/admin/%s/%s/%s" target="_blank" >%s</a><br>' \
    #                       % (item._meta.app_label, item._meta.model_name, item.id, item.name)
    #     return output
    #
    # building_link.allow_tags = True
    # building_link.short_description = 'Buildings'

    def has_add_permission(self, request):
        return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('email',)
    search_fields = ('email', 'username')
    list_display = ['email', 'username', 'photo_img', 'is_active',
                    'is_blocked', 'date_joined', 'social_info']
    fields = ('username', 'email', 'photo', 'is_active', 'is_blocked',
              'email_notification', 'push_notification', 'date_joined', 'last_login',
              'is_social_user')
    # exclude = ('groups', 'user_permissions', 'email_new', 'password')
    readonly_fields = ('date_joined', 'last_login')
    list_filter = ()
    form = UserForm
    inlines = [UserSocialInlineAdmin]

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        return queryset.prefetch_related('user_social')

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
