from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

api_router = routers.DefaultRouter()
api_router.register(r'codex', views.CodexViewSet, basename='codex')
api_router.register(r'information', views.InformationViewSet, basename='information')
api_router.register(r'pages', views.PageViewSet, basename='page')
api_router.register(r'tasks', views.TaskViewSet, basename='task')
api_router.register(r'notes', views.NoteViewSet, basename='note')

urlpatterns = [
  path("api/", include(api_router.urls), name="api"),
  path('api-auth/', obtain_auth_token, name='api_auth'),
]
