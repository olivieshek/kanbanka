from django.shortcuts import render
# from .models import
from django.conf import settings
from django.views.generic import *  # встроенные views


class DeskListView(ListView):
    model = None  # TODO model = Desk

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context
