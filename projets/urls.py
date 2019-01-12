from django.urls import path
from . import views

urlpatterns = [
    path("codex", views.codex_list_view, name="codex"),
    path("codex/add", views.codex_add_view, name="codex_add"),
    path("codex/<slug:codex_slug>", views.codex_details_view, name="codex_details"),
    path(
        "codex/<slug:codex_slug>/information",
        views.information_view,
        name="information",
    ),
    path("tasks", views.task_list_view, name="tasks"),
    path(
        "codex/<slug:codex_slug>/tasks",
        views.task_list_filtered_view,
        name="codex_tasks",
    ),
    path("tasks/<int:task_id>", views.task_details_view, name="task_details"),
    path("notes", views.note_list_view, name="notes"),
    path("notes/<int:note_id>", views.note_details_view, name="note_details"),
    path("text-editor", views.text_editor_view, name="text_editor"),
]
