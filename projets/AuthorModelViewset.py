from rest_framework import viewsets, permissions


class AuthorModelViewSet(viewsets.GenericViewSet):
    """
    Custom ViewSet to check the permission of the current user
    """
    author_filter_arg = None

    def __init__(self, **kwargs):
        self.permission_classes.append(permissions.IsAuthenticated)
        super().__init__(**kwargs)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        # Allow to set the field to check the author against
        queryset = super().get_queryset()
        if not self.request or not queryset or not self.author_filter_arg:
            return None
        user = self.request.user
        filter_arg = self.author_filter_arg
        return queryset.filter(**{filter_arg: user})


class CreationModelViewSet(viewsets.GenericViewSet):
    """
    Custom ViewSet which allow to specify a different serializer for creation of the model
    """
    create_serializer_class = None

    def get_serializer_class(self):
        # Allow to specify a different serializer for creation
        serializer_class = self.serializer_class
        if self.action == 'create' and self.create_serializer_class is not None:
            serializer_class = self.create_serializer_class
        return serializer_class
