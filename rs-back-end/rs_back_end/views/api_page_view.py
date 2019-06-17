from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from rs_back_end.AuthorModelViewset import AuthorModelViewSet
from rs_back_end.models import Page, Task
from rs_back_end.serializers import PageSerializer


class PageViewSet(AuthorModelViewSet, viewsets.ReadOnlyModelViewSet):
  """
  API Endpoint that allows page to be viewed
  """
  queryset = Page.objects.all().order_by('-date') \
    .prefetch_related(
    Prefetch('tasks',
             queryset=Task.objects.all().order_by('-creation_date')))
  author_filter_arg = "codex__author"
  serializer_class = PageSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_fields = ('codex__slug', 'date',)
