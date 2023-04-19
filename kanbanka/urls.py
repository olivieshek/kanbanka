from django.urls import path
from .views import (
    KanbanListView,
    KanbanCreateView,
    KanbanDeleteView,
    KanbanDetailView,
    UserLoginView,
    UserLogoutView,
    TaskCreateView
    # UserSignupView,
)

appname = "kanbanka"

urlpatterns = [
    path('', KanbanListView.as_view(), name='index'),
    path('add_kanban/', KanbanCreateView.as_view(), name="kanban_create"),
    path('add_task/', TaskCreateView.as_view(), name='task_create'),
    path('delete_kanban/<int:pk>', KanbanDeleteView.as_view(), name="kanban_delete"),
    path('kanban_detail/<int:pk>', KanbanDetailView.as_view(), name="kanban_detail"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", UserLogoutView.as_view(), name="logout"),
    # path("accounts/signup/", UserSignup, name="signup"),
]
