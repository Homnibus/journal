from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from rs_back_end.commun.utils import java_string_hashcode, create_or_get_today_page
from rs_back_end.fields import AuthorFilteredPrimaryKeyRelatedField
from rs_back_end.models import Codex, Page, Note, Task, Information, get_current_timestamp


class HashSerializerMixin(serializers.Serializer):
  initial_hash = serializers.SerializerMethodField()

  def get_initial_hash(self, obj):
    return java_string_hashcode(getattr(obj, self.Meta.hash_field))


class HashUpdateSerializerMixin(serializers.Serializer):
  modification_hash = serializers.IntegerField(write_only=True)

  def validate_modification_hash(self, value):
    initial_hash = java_string_hashcode(
      getattr(self.instance, self.Meta.hash_field)
    )
    if initial_hash != value:
      raise serializers.ValidationError(
        gettext(
          "The {resource_name} have been modified since the last modification attempt."
        ).format(resource_name=self.Meta.model._meta.object_name)
      )
    return value


class CodexSerializer(serializers.ModelSerializer):
  author = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Codex
    fields = "__all__"
    read_only_fields = ("slug",)


class NoteSerializer(
  HashUpdateSerializerMixin, HashSerializerMixin, serializers.ModelSerializer
):
  class Meta:
    model = Note
    fields = "__all__"
    hash_field = "text"


class NoteCreateSerializer(HashSerializerMixin, serializers.ModelSerializer):
  codex = serializers.IntegerField(min_value=1, write_only=True)

  class Meta:
    model = Note
    fields = "__all__"
    hash_field = "text"

  def validate_codex(self, value):
    codex = Codex.objects.filter(id=value).first()
    if codex is None:
      raise serializers.ValidationError(
        gettext("The specified Codex does not exist.")
      )
    if not self.context['request'].user.has_perm('rs_back_end.change_codex', codex):
      raise PermissionDenied()
    return value

  def validate(self, data):
    # Check if the note of the day does not already exist for the codex
    today = get_current_timestamp().date()
    if Note.objects.filter(
      page__codex__id=data["codex"], page__date=today
    ).exists():
      raise serializers.ValidationError(
        gettext("The Note of the day already exist for this Codex.")
      )
    return data

  def create(self, validated_data):
    # Get the page to link the note and add it to the validated data
    page = create_or_get_today_page(validated_data["codex"])
    validated_data["page"] = page
    # Get off the codex from the validated data so the creation of the note will not trigger an unexpected
    # keyword argument
    validated_data.pop("codex")
    # Save the note
    note = super().create(validated_data)
    return note


class TaskSerializer(
  HashUpdateSerializerMixin, HashSerializerMixin, serializers.ModelSerializer
):
  class Meta:
    model = Task
    fields = "__all__"
    hash_field = "text"


class TaskCreateSerializer(serializers.ModelSerializer, HashSerializerMixin):
  codex = serializers.IntegerField(min_value=1, write_only=True)

  class Meta:
    model = Task
    fields = "__all__"
    hash_field = "text"
    extra_kwargs = {'is_achieved': {'required': False}}

  def validate_codex(self, value):
    codex = Codex.objects.filter(id=value).first()
    if codex is None:
      raise serializers.ValidationError(
        gettext("The specified Codex does not exist.")
      )
    if not self.context['request'].user.has_perm('rs_back_end.change_codex', codex):
      raise PermissionDenied()
    return value

  def create(self, validated_data):
    # Get the page to link the task and add it to validated data
    page = create_or_get_today_page(validated_data["codex"])
    validated_data["page"] = page
    # Get off the codex from the validated data so the creation of the task will not trigger an unexpected
    # keyword argument
    validated_data.pop("codex")
    # Save the task
    task = super().create(validated_data)
    return task


class PageSerializer(serializers.ModelSerializer):
  note = NoteSerializer(read_only=True, many=False)
  tasks = TaskSerializer(read_only=True, many=True)

  class Meta:
    model = Page
    fields = "__all__"


class InformationSerializer(
  HashUpdateSerializerMixin, HashSerializerMixin, serializers.ModelSerializer
):
  class Meta:
    model = Information
    fields = "__all__"
    hash_field = "text"


class InformationCreateSerializer(serializers.ModelSerializer, HashSerializerMixin):
  codex = AuthorFilteredPrimaryKeyRelatedField(
    queryset=Codex.objects.all(), allow_null=False, required=True
  )

  def validate_codex(self, value):
    if Information.objects.filter(codex=value).exists():
      raise ValidationError(
        gettext("The specified Information already exist.")
      )
    return value

  class Meta:
    model = Information
    fields = "__all__"
    hash_field = "text"
    extra_kwargs = {"codex": {"allow_null": False, "required": True}}
