from django.urls import path
from .views import *

urlpatterns = [
    path('', DeskListView.as_view(), name='index'),
]
