from .models import Kanban, Task
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import generic as g  # встроенные views
from django.contrib import messages
from django.contrib.auth import views as authviews
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect

"""
-- Available Views:
. Kanban Create
. Kanban Detail (== Task List)
. Kanban Update
. Kanban Delete
. Task Create
. Task Detail
. Task Update
. Task Delete
. User Sign Up
. User Login
. User Logout
"""

# - Task Detail View
# TODO - Kanban Update
# TODO - профиль аккаунта
# TODO - подтверждение аккаунта почтой
# TODO - восстановление / изменение пароля
# TODO - просрочка для Task
# TODO - инвайт-система
# TODO - css (относительно нормальный дизайн)
# TODO - получать дату/время одной строкой(?), а потом уже разбивать на части


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
    success_url = reverse_lazy("kanbanka:index")


class KanbanListView(g.ListView):
    model = Kanban
    template_name = "kanbanka/index.html"
    context_object_name = "kanbans"  # default - object_list

    # def get_queryset(self):
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         return Kanban.objects.none()
    #
    #     kanbans = Kanban.objects.filter(Q(owner=user) | Q(kanban_tasks__executor=user)).distinct()
    #     return kanbans

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["kanban_owner"] = self.object_list.filter(Q(owner=self.request.user)).distinct()
            context["kanban_member"] = self.object_list.filter(Q(kanban_tasks__executor=self.request.user)).distinct()
        return context


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
    success_url = reverse_lazy("kanbanka:index")
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


def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            form.save()
            user = authenticate(
                username=username,
                password=password
            )
            if user is not None:
                # Создавать пользователя только с подтвержденной учеткой (if user.is_active)
                login(request, user)
            else:
                messages.error(request, 'Invalid Log in.')
                return reverse_lazy('kanbanka:index')
            return HttpResponseRedirect("/kanbanka/")
    else:
        form = UserCreationForm()

    return render(request, "authentication/signup.html", {"form": form})


class TaskCreateView(g.CreateView):
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
            if not form.cleaned_data["executor"]:
                form.add_error("executor", "Назначьте исполнителя!")
                return super().form_invalid(form)
            if not form.cleaned_data["deadline_date"]:
                form.add_error("deadline_date", "Назначьте дату дедлайна!")
                return super().form_invalid(form)
            if not form.cleaned_data["deadline_time"]:
                form.add_error("deadline_time", "Назначьте время дедлайна!")
                return super().form_invalid(form)
            self.object.status = "ACTIVE"
            self.object.assigned_date = timezone.now().date()
            self.object.assigned_time = timezone.now().time()

        return super().form_valid(form)


class TaskCompleteView(g.UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Task
    fields = []
    current_timezone = timezone.now()
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


# Задача, страница "подробнее"
class TaskDetailView(g.DetailView):
    model = Task
    template_name = "kanbanka/task_detail.html"
    context_object_name = "task"


# ЗАДАЧИ ЮЗЕРА
class TaskUserListView(g.ListView):
    model = Task
    template_name = "kanbanka/user_tasks.html"
    context_object_name = "tasks"  # default - object_list

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()

        tasks = Task.objects.filter(Q(executor=user))
        return tasks