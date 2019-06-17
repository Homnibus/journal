from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

api_router = routers.DefaultRouter()
api_router.register(r'codex', views.CodexViewSet, base_name='codex')
api_router.register(r'information', views.InformationViewSet, base_name='information')
api_router.register(r'pages', views.PageViewSet, base_name='page')
api_router.register(r'tasks', views.TaskViewSet, base_name='task')
api_router.register(r'notes', views.NoteViewSet, base_name='note')

urlpatterns = [
    path("codex", views.codex_list_view, name="codex"),
    path("codex/add", views.codex_add_view, name="codex_add"),
    path("codex/<slug:codex_slug>", views.codex_details_view, name="codex_details"),
    path(
        "codex/<slug:codex_slug>/information",
        views.information_details_view,
        name="information",
    ),
    path(
        "codex/<slug:codex_slug>/informations",
        views.information_list_view,
        name="informations",
    ),
    path("tasks", views.task_list_filtered_view, name="tasks_list"),
    path("codex/<slug:codex_slug>/tasks", views.task_list_view, name="tasks"),
    path("tasks/<int:task_id>", views.task_details_view, name="task_details"),
    path("codex/<slug:codex_slug>/notes", views.note_list_view, name="notes"),
    path("notes/<int:note_id>", views.note_details_view, name="note_details"),
    path("text-editor", views.text_editor_view, name="text_editor"),

    path("api/", include(api_router.urls), name="api"),
    path("api/codex/<slug:codex_slug>", views.codex_details_view, name="codex_details"),
    path('api-auth/', obtain_auth_token, name='api_auth'),
]
