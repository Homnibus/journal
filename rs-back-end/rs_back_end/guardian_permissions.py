from rest_framework import permissions
from rs_back_end.models import Codex


class IsCodexAuthor(permissions.BasePermission):
    """
     Return False in case of creation of a object linked to a codex,  if the codex exist and was not created by the user
    """
    def has_permission(self, request, view):

        if view.action == 'create':
            codex_id = request.data.get('codex_id')
            if codex_id:
                codex = Codex.objects.filter(id=codex_id)
                if codex.exists() and not codex.first().author == request.user:
                    return False

        return True

class FullObjectPermissions(permissions.DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
