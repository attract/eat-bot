from django.conf import settings

from django.shortcuts import render
from django.views.generic import View
from core.bl.utils_helper import prn


class HomeView(View):

    def get(self, request):
        context = dict()
        return render(request, 'home.html', context=context)
