from django.urls import path
from .views import KanbanListView, KanbanCreateView, KanbanDeleteView, KanbanDetailView, UserLoginView, UserLogoutView

appname = "kanbanka"

urlpatterns = [
    path('', KanbanListView.as_view(), name='index'),
    path('add_kanban/', KanbanCreateView.as_view(), name="kanban_create"),
    path('delete_kanban/<int:pk>', KanbanDeleteView.as_view(), name="kanban_delete"),
    path('kanban_detail/<int:pk>', KanbanDetailView.as_view(), name="kanban_detail"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", UserLogoutView.as_view(), name="logout"),
]
