from .models import Kanban, Task
from django.conf import settings
from django.shortcuts import render
from django.views import generic as g  # встроенные views
from django.contrib.auth import views as authviews
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

"""
-- Available Views:
1. Kanban Create
2. 
"""

# TODO "Update" Kanban


class KanbanCreateView(g.CreateView):
    model = Kanban
    template_name = "kanbanka/kanban_create.html"
    fields = '__all__'
    success_url = reverse_lazy("index")


class KanbanListView(g.ListView):
    model = Kanban
    template_name = "kanbanka/index.html"
    context_object_name = "kanbans"  # default - object_list

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['MEDIA_URL'] = settings.MEDIA_URL
    #     return context


class KanbanDetailView(g.DetailView):
    model = Kanban
    template_name = "kanbanka/kanban_detail.html"
    context_object_name = "kanban"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.kanban_tasks
        context["tasks_planned"] = Task.objects.filter(status='PLANNED')
        context["tasks_active"] = Task.objects.filter(status='ACTIVE')
        context["tasks_completed"] = Task.objects.filter(status='COMPLETED')
        context["tasks_overdue"] = Task.objects.filter(status='OVERDUE')
        return context


class KanbanDeleteView(g.DeleteView):
    model = Kanban
    success_url = reverse_lazy("index")
    template_name = "kanbanka/kanban_delete.html"


class UserLoginView(authviews.LoginView):
    fields = "__all__"
    template_name = "authentication/login.html"


class UserLogoutView(authviews.LogoutView):
    next_page = reverse_lazy('index')

# TODO User SignUp


class TaskCreateView(g.CreateView):
    # TODO Создавать может только хозяин доски?
    model = Task
    template_name = 'kanbanka/task_create.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.kanban = Kanban.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        kanban_pk = self.object.kanban.id
        return reverse(
            'kanbanka:kanban_detail',
            kwargs={'pk': kanban_pk}
        )


class TaskDeleteView(g.DeleteView):
    model = Task
    template_name = "kanbanka/task_delete.html"
    next_page = reverse_lazy("index")

    def get_success_url(self):
        kanban_pk = self.object.kanban.pk
        return reverse_lazy(
            'kanbanka:kanban_detail',
            kwargs={'pk': kanban_pk}
        )
