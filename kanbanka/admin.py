from django.contrib import admin
from .models import Kanban

admin.site.site_url = '/kanbanka/'
admin.site.register(Kanban)
