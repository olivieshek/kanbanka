from django.urls import path
from .views import KanbanListView, KanbanCreateView, KanbanDeleteView, KanbanDetailView

appname = "kanbanka"

urlpatterns = [
    path('', KanbanListView.as_view(), name='index'),
    path('add_kanban/', KanbanCreateView.as_view(), name="kanban_create"),
    path('delete_kanban/<int:pk>', KanbanDeleteView.as_view(), name="kanban_delete"),
    path('kanban_detail/<int:pk>', KanbanDetailView.as_view(), name="kanban_detail"),
]
