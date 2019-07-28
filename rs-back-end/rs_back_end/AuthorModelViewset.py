from rest_framework import viewsets

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
