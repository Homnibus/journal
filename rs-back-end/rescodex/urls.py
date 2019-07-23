from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
                path("admin/", admin.site.urls),
                path("", include("rs_back_end.urls")),
                path("", TemplateView.as_view(template_name='rs_back_end/index.html')),
                path("<path:path>", TemplateView.as_view(template_name='rs_back_end/index.html'))
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
