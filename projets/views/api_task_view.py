from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_guardian.filters import DjangoObjectPermissionsFilter

from projets.AuthorModelViewset import CreationModelViewSet
from projets.models import Task
from projets.permissions import FullObjectPermissions
from projets.serializers import TaskSerializer, TaskCreateSerializer


class TaskViewSet(CreationModelViewSet, viewsets.ModelViewSet):
    """
    API Endpoint that allows tasks to be viewed or edited
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    create_serializer_class = TaskCreateSerializer
    permission_classes = (FullObjectPermissions,)
    filter_backends = (DjangoObjectPermissionsFilter, DjangoFilterBackend,)
    filterset_fields = ('page__codex__slug', 'is_achieved')
