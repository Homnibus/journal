from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_guardian.filters import DjangoObjectPermissionsFilter

from rs_back_end.models import Page, Task
from rs_back_end.serializers import PageSerializer
from rs_back_end.guardian_permissions import FullObjectPermissions


class PageViewSet(viewsets.ReadOnlyModelViewSet):
  """
  API Endpoint that allows page to be viewed
  """
  queryset = Page.objects.all().order_by('-date') \
    .prefetch_related(
    Prefetch('tasks',
             queryset=Task.objects.all().order_by('-creation_date')))
  serializer_class = PageSerializer
  permission_classes = (FullObjectPermissions,)
  filter_backends = (DjangoObjectPermissionsFilter, DjangoFilterBackend,)
  filterset_fields = ('codex__slug', 'date',)
