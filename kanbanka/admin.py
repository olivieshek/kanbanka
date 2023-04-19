from django.contrib import admin
from .models import Kanban, Task

admin.site.site_url = '/kanbanka/'
admin.site.register(Kanban)
admin.site.register(Task)
