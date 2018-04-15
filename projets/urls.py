from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
url(r'^connexion$', auth_views.login, {'template_name': 'projets/connexion.html'}, name='connexion'),
url(r'^deconnexion$', auth_views.logout, {'template_name': 'projets/deconnexion.html'}, name='deconnexion'),
url(r'^accueil$', views.afficher_derniers_codex, name='accueil'),	
url(r'^derniers-codex$', views.afficher_derniers_codex, name='afficher_derniers_codex'),	
url(r'^nouveau-codex$', views.creer_codex, name='nouveau_codex'),
url(r'^projets/(?P<slug>.+)/codex$', views.afficher_codex, name='afficher_codex'),
url(r'^projets/(?P<slug>.+)/maj-journal$', views.maj_journal, name='maj_journal'),
url(r'^projets/(?P<slug>.+)/maj-todo$', views.maj_todo, name='maj_todo'),
url(r'^projets/(?P<slug>.+)/main-courante$', views.afficher_main_courante, name='afficher_main_courante'),
url(r'^projets/(?P<slug>.+)/maj-main-courante$', views.maj_main_courante, name='maj_main_courante'),
url(r'^projets/(?P<slug>.+)/contact$', views.afficher_contact_liste, name='afficher_contact_liste'),
url(r'^projets/(?P<slug>.+)/maj-contact$', views.maj_contact_liste, name='maj_contact_liste'),
url(r'^projets/(?P<slug>.+)/taches$', views.afficher_taches, name='afficher_taches'),
url(r'^projets/(?P<slug>.+)/taches/(?P<page_number>\d+)$', views.afficher_taches, name='afficher_taches'),
]


