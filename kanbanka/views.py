from .models import Kanban
from django.conf import settings
from django.shortcuts import render
from django.views import generic as g  # встроенные views
from django.urls import reverse_lazy


class KanbanCreateView(g.CreateView):
    model = Kanban
    template_name = "kanbanka/kanban_create.html"
    fields = '__all__'
    success_url = reverse_lazy("index")


class KanbanListView(g.ListView):
    model = Kanban
    template_name = "kanbanka/index.html"
    context_object_name = "kanbans"  # default - object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


class KanbanDetailView(g.DetailView):
    model = Kanban
    template_name = "kanbanka/kanban_detail.html"


class KanbanDeleteView(g.DeleteView):
    model = Kanban
    template_name = "kanbanka/kanban_delete.html"
    success_url = reverse_lazy("index")
