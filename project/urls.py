from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
from rest_framework.routers import DefaultRouter

from core.static import static
from home.views import HomeView
from rest_framework_swagger.views import get_swagger_view

from users.views import ActivateUserView, PasswordRecoveryConfirmView, UserViewSet, EmailConfirmView, \
    ActivateSocialAccountView

schema_view = get_swagger_view(title='Swagger API')

handler403 = 'core.views.page_403'
handler404 = 'core.views.page_404'
handler500 = 'core.views.page_500'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^docs/', schema_view),
    # url(r'^admin/logout/$', logout, {'next_page': 'login'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^', include('pages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
