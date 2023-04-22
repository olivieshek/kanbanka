from django.urls import path
from .views import (
    KanbanListView,
    KanbanCreateView,
    KanbanDeleteView,
    KanbanDetailView,
    UserLoginView,
    UserLogoutView,
    TaskCreateView,
    TaskDeleteView,
    # UserSignupView,
)

appname = "kanbanka"
urlpatterns = [
    path('', KanbanListView.as_view(), name='index'),
    path('add_kanban/', KanbanCreateView.as_view(), name="kanban_create"),
    path('kanban_delete/<int:pk>', KanbanDeleteView.as_view(), name="kanban_delete"),
    path('kanban/detail/<int:pk>', KanbanDetailView.as_view(), name="kanban_detail"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", UserLogoutView.as_view(), name="logout"),
    path('kanban/task_create/', TaskCreateView.as_view(), name='task_create'),
    path("kanban/task_delete/<int:pk>", TaskDeleteView.as_view(), name="task_delete"),
    # path("accounts/signup/", UserSignup, name="signup"),
]

