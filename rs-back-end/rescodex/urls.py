from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
                path("admin/", admin.site.urls),
                path(
                  "connexion",
                  auth_views.LoginView.as_view(template_name="rs_back_end/connexion.html"),
                  name="connexion",
                ),
                path(
                  "deconnexion",
                  auth_views.LogoutView.as_view(template_name="rs_back_end/disconnection.html"),
                  name="disconnection",
                ),
                path("", RedirectView.as_view(url="codex"), name="home"),
                path("", include("rs_back_end.urls")),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
