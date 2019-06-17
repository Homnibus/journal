from rest_framework import viewsets
from rest_framework_guardian import filters

from projets.models import Codex
from projets.permissions import FullObjectPermissions
from projets.serializers import CodexSerializer


class CodexViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows tasks to be viewed or edited
    """
    queryset = Codex.objects.all().order_by('-nested_update_date')
    serializer_class = CodexSerializer
    lookup_field = 'slug'
    permission_classes = (FullObjectPermissions,)
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
