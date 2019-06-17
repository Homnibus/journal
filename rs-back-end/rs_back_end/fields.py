from rest_framework import serializers


class AuthorFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
  def get_queryset(self):
    request = self.context.get('request', None)
    queryset = super().get_queryset()
    if not request or not queryset:
      return None
    return queryset.filter(author=request.user)
