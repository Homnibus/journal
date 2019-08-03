from rest_framework import viewsets
from rest_framework_guardian.filters import DjangoObjectPermissionsFilter

from rs_back_end.models import Codex
from rs_back_end.guardian_permissions import FullObjectPermissions
from rs_back_end.serializers import CodexSerializer


class CodexViewSet(viewsets.ModelViewSet):
  """
  API Endpoint that allows tasks to be viewed or edited
  """
  queryset = Codex.objects.all().order_by('-nested_update_date')
  serializer_class = CodexSerializer
  lookup_field = 'slug'
  permission_classes = (FullObjectPermissions,)
  filter_backends = (DjangoObjectPermissionsFilter,)
