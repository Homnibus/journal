from rest_framework import serializers
from projets.models import Codex, Page, Note, Task, Information


class CodexSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Codex
        exclude = ("slug",)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ("codex",)


class NoteSerializer(serializers.ModelSerializer):
    codex = serializers.ReadOnlyField(source="page.codex")
    page = serializers.IntegerField(required=False)

    class Meta:
        model = Note
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    codex = serializers.ReadOnlyField(source="page.codex")
    page = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = "__all__"


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"
        read_only_fields = ("codex",)
