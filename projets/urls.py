from django.urls import path
from . import views

urlpatterns = [
path('derniers-codex/', views.afficher_derniers_codex, name='afficher_derniers_codex'),	
path('nouveau-codex/', views.creer_codex, name='nouveau_codex'),
path('taches/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
path('taches/<int:page_number>/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
path('taches/<int:page_number>/<str:sort_by>/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
path('taches/<int:page_number>/<str:sort_by>/<str:sort_way>/', views.afficher_taches_toutes, name='afficher_taches_toutes'),
path('<slug:slug>/codex', views.afficher_codex, name='afficher_codex'),
path('<slug:slug>/maj-journal', views.maj_journal, name='maj_journal'),
path('<slug:slug>/rest-tache', views.rest_tache, name='rest_tache'),
path('<slug:slug>/rest-page', views.rest_page, name='rest_page'),
path('<slug:slug>/main-courante', views.afficher_main_courante, name='afficher_main_courante'),
path('<slug:slug>/maj-main-courante', views.maj_main_courante, name='maj_main_courante'),
path('<slug:slug>/taches', views.afficher_taches, name='afficher_taches'),
path('<slug:slug>/taches/<int:page_number>/', views.afficher_taches, name='afficher_taches'),
]


