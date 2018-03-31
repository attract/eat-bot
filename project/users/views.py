from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from authentication.permissions import IsAuthenticatedCore
from core.bl.utils_helper import prn
from core.mixins import ExpandMixin, SearchMixin, ProductServices
from core.utils import EmailNotification
from core.views import DeepLinkPageView
from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, UserSocialSerializer


class ActivateUserView(View):

    def get(self, request, uidb64, token):
        context = dict()
        template = 'registration/activation_user_result.html'

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid).first()
        context['error'] = ''

        if not user:
            context['error'] = 'user_not_found'

        if not default_token_generator.check_token(user, token):
            context['error'] = 'invalid_token'

        if user.is_social_user:
            # activate standart user account
            user.is_social_user = False
        elif user.is_active:
            context['error'] = 'already_activated'

        if not context['error']:
            user.is_active = True
            user.save()

        return render(request, template, context=context)


class ActivateSocialAccountView(View):

    def get(self, request, provider, uidb64, token):
        context = dict()
        template = 'registration/activation_user_result.html'

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid).first()
        context['error'] = ''

        if not user:
            context['error'] = 'user_not_found'

        if not default_token_generator.check_token(user, token):
            context['error'] = 'invalid_token'

        if provider in dict(settings.SOCIAL_PROVIDER).keys():
            user_social = user.user_social.filter(provider=provider).first()
            if user_social:
                if user_social.is_active:
                    context['error'] = 'already_activated'
                else:
                    # activating social account
                    user_social.is_active = True
                    user_social.save()
            else:
                context['error'] = 'user_not_found'

        return render(request, template, context=context)


class PasswordRecoveryConfirmView(View):

    def get(self, request, uidb64, token):
        context = dict()

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid).first()
        context['error'] = ''
        if not default_token_generator.check_token(user, token):
            context['error'] = 'invalid_token'

        if not context['error']:
            from django.http.response import HttpResponseRedirectBase
            HttpResponseRedirectBase.allowed_schemes += ['lulu']
            redirect_url = 'lulu://password-recovery/%s/%s' % (uidb64, token)

            if not request.is_mobile:
                return render(request, 'need_redirect_to_app.html', context=context)

            prn('REDIRECT TO APP URL: %s' % redirect_url)
            return DeepLinkPageView.redirect_by_url(redirect_url)

            # return HttpResponseRedirect(redirect_url)

        return render(request, '404.html', context=context)


class EmailConfirmView(View):

    def get(self, request, uidb64, token):
        context = dict()

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid).first()
        context['error'] = ''
        if not user:
            context['error'] = 'user_not_found'
        else:
            if not user.email_new:
                context['error'] = 'user_not_found'

        if not default_token_generator.check_token(user, token):
            context['error'] = 'invalid_token'

        if not context['error']:
            user.email = user.email_new
            user.email_new = None
            user.save(update_fields=['email', 'email_new'])

        return render(request, 'profile/email_change_result.html', context=context)


class UserViewSet(ExpandMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Creates, Updates, and retrieves User accounts \n
    """
    queryset = User.objects.prefetch_related('user_social').all()
    serializer_class = UserSocialSerializer
    permission_classes = (IsAuthenticatedCore, IsOwnerOrReadOnly)
    # filter_backends = (filters.SearchFilter,)
    page_size_query_param = 'page_size'
    max_page_size = 20
    expandable = {}

    def get_queryset(self):
        return self.queryset.prefetch_related('user_reported_report')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'email_new' in request.data and request.data['email_new'] != instance.email:
            # if updating email, send confirmation message to user
            notification = EmailNotification(instance)
            notification.send_new_email_confirm_link()

        if 'photo_clear' in request.data and request.data['photo_clear']:
            instance.photo.delete()

        response = ProductServices.expands(request, instance, serializer.data, self.expandable)
        return Response(response)
