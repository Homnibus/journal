from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import include
from django.conf import settings
from projets import views as journal_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('connexion/', auth_views.login, {'template_name': 'projets/connexion.html'}, name='connexion'),
    path('deconnexion/', auth_views.logout, {'template_name': 'projets/deconnexion.html'}, name='deconnexion'),
    path('accueil/', journal_views.afficher_derniers_codex, name='accueil'),	
    path('projets/', include('projets.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
