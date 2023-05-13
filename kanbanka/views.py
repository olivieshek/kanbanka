from .models import Kanban, Task
from django.conf import settings
from django.shortcuts import render
from django.views import generic as g  # встроенные views
from django.contrib.auth import views as authviews
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import HttpResponseRedirect

"""
-- Available Views:
1. Kanban Create
2. 
"""

# TODO "Update" Kanban

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get("django_timezone")
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)


class KanbanCreateView(LoginRequiredMixin, g.CreateView):
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


class KanbanDeleteView(LoginRequiredMixin, UserPassesTestMixin, g.DeleteView):
    model = Kanban
    success_url = reverse_lazy("index")
    template_name = "kanbanka/kanban_delete.html"

    def test_func(self) -> bool | None:
        kanban = get_object_or_404(Kanban, pk=self.kwargs.get('pk'))
        return kanban.owner

    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")


class UserLoginView(authviews.LoginView):
    fields = "__all__"
    template_name = "authentication/login.html"


class UserLogoutView(authviews.LogoutView):
    next_page = reverse_lazy('kanbanka:index')

# TODO User SignUp


class TaskCreateView(g.CreateView):
    model = Task
    template_name = 'kanbanka/task_create.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.kanban = Kanban.objects.get(id=self.kwargs['pk'])
        self.object.summary = self.object.description[:50]
        return super().form_valid(form)

    def get_success_url(self):
        kanban_pk = self.object.kanban.id
        return reverse(
            'kanbanka:kanban_detail',
            kwargs={
                'pk': kanban_pk,
            }
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


class TaskActivateView(g.UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Task
    fields = [
        "executor",
        "deadline_date",
        "deadline_time",
    ]
    template_name = "kanbanka/task_activate.html"

    def get_success_url(self):
        kanban_pk = self.object.kanban.id
        return reverse(
            'kanbanka:kanban_detail',
            kwargs={'pk': kanban_pk}
        )

    def form_valid(self, form):
        if self.object.status == "PLANNED":
            self.object.status = "ACTIVE"
            self.object.assigned_date = timezone.now().date()
            self.object.assigned_time = timezone.now().time()

        return super().form_valid(form)


class TaskCompleteView(g.UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Task
    fields = []
    current_timezone = timezone.now()
    # TODO ставить завершение задним числом
    template_name = "kanbanka/task_complete.html"

    def get_success_url(self):
        kanban_pk = self.object.kanban.id
        return reverse(
            'kanbanka:kanban_detail',
            kwargs={'pk': kanban_pk}
        )

    def form_valid(self, form):
        if self.object.status == "ACTIVE":
            self.object.status = "COMPLETED"
            self.object.completed_date = timezone.now().date()
            self.object.completed_time = timezone.now().time()

        return super().form_valid(form)