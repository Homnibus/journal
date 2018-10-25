from django.urls import path
from . import views

urlpatterns = [
    path('taches/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
    path('taches/<int:page_number>/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
    path('taches/<int:page_number>/<str:sort_by>/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
    path(
        'taches/<int:page_number>/<str:sort_by>/<str:sort_way>/',
        views.afficher_taches_toutes,
        name='afficher_taches_toutes'
    ),

    path('<slug:slug>/taches', views.afficher_taches, name='afficher_taches'),
    path('<slug:slug>/taches/<int:page_number>/', views.afficher_taches, name='afficher_taches'),


    path('new-codex/', views.new_codex_view, name='new_codex'),
    path('<slug:codex_slug>/codex', views.codex_view, name='codex'),
    path('<slug:codex_slug>/task', views.task_view, name='task'),
    path('<slug:codex_slug>/note', views.note_view, name='note'),
    path('<slug:codex_slug>/codex-info', views.codex_info_view, name='codex_info'),
]
