from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.urls import resolve
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View

from core.bl.utils_helper import prn


def page_403(request):
    # to check it add in view function
    # raise PermissionDenied
    response = render(request, "403.html")
    response.status_code = 403
    return response


def page_404(request):
    prn('404')
    response = render(request, "404.html")
    response.status_code = 404
    return response


def page_500(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


class DeepLinkPageView(View):

    def get(self, request, id_obj=None):

        current_url = resolve(request.path_info).url_name
        if current_url == 'photo-deep-link':
            redirect_url = 'luluphoto://%s' % id_obj

        elif current_url == 'user-deep-link':
            redirect_url = 'luluuser://%s' % id_obj

        print('REDIRECT TO APP URL: %s' % redirect_url)
        response = HttpResponse("", status=302)
        response['Location'] = redirect_url
        return self.redirect_by_url(redirect_url)

        #return HttpResponseRedirect(redirect_url)

    @classmethod
    def redirect_by_url(cls, redirect_url):
        print('REDIRECT TO APP URL: %s' % redirect_url)
        response = HttpResponse("", status=302)
        response['Location'] = redirect_url
        return response
