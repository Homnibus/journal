from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_guardian.filters import DjangoObjectPermissionsFilter

from projets.AuthorModelViewset import CreationModelViewSet
from projets.models import Note
from projets.permissions import FullObjectPermissions
from projets.serializers import NoteSerializer, NoteCreateSerializer


class NoteViewSet(CreationModelViewSet, viewsets.ModelViewSet):
    """
    API Endpoint that allows note to be viewed or edited
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    create_serializer_class = NoteCreateSerializer
    permission_classes = (FullObjectPermissions,)
    filter_backends = (DjangoObjectPermissionsFilter, DjangoFilterBackend,)
    filterset_fields = ('page__codex__slug',)
