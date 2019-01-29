from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea, HiddenInput, CheckboxInput, IntegerField
from django.utils.translation import gettext

from projets.commun.utils import java_string_hashcode
from .models import Codex, Information, Note, Task, get_current_timestamp, Page


class AbstractHashFrom(ModelForm):
    hash = IntegerField(
        label="hash", required=True, widget=HiddenInput(attrs={"class": "hash"})
    )
    # For render purpose only. Should not be validated.
    id = IntegerField(
        label="id", required=False, widget=HiddenInput(attrs={"class": "id"})
    )

    def __init__(self, data=None, instance=None, *args, **kwargs):
        super(AbstractHashFrom, self).__init__(
            data=data, instance=instance, *args, **kwargs
        )
        # If an instance is given, update the hash
        if instance:
            self.initial["hash"] = java_string_hashcode(
                getattr(instance, self.Meta.hash_field)
            )
            self.initial["id"] = instance.id

    def clean_hash(self):
        input_hash = self.cleaned_data["hash"]
        # If there is not error the hash, check if the hash is the same as in the database
        current_hash = java_string_hashcode(self.instance.text)
        if current_hash != input_hash:
            raise ValidationError(
                gettext(
                    "The {resource_name} have been modified since the last modification attempt."
                ).format(resource_name=self.Meta.model._meta.object_name)
            )

        return input_hash


class CodexForm(ModelForm):
    class Meta:
        model = Codex
        fields = ("title", "description")
        widgets = {
            "description": Textarea(
                attrs={"rows": 3, "style": "resize:none;", "class": "codex_text"}
            )
        }

    def save(self, commit=True, author=None, *args, **kwargs):
        """ Override the save method to manage the author """
        codex = super(CodexForm, self).save(commit=False)
        # The page must be given otherwise the note can't be create
        codex.author = author
        if commit:
            codex.save()
        return codex


class InformationCreateForm(ModelForm):
    class Meta:
        model = Information
        fields = ("text",)
        widgets = {
            "text": Textarea(
                attrs={"rows": 3, "style": "resize:none;", "class": "information_text"}
            )
        }

    def __init__(self, codex=None, *args, **kwargs):
        super(InformationCreateForm, self).__init__(*args, **kwargs)
        # The codex is needed to save the form
        if codex is not None:
            self.codex = codex

    def save(self, commit=True, *args, **kwargs):
        information = super(InformationCreateForm, self).save(commit=False)
        information.codex = self.codex
        if commit:
            information.save()
        return information


class InformationUpdateForm(AbstractHashFrom):
    class Meta:
        model = Information
        fields = ("text",)
        hash_field = "text"
        widgets = {
            "text": Textarea(
                attrs={"rows": 3, "style": "resize:none;", "class": "information_text"}
            )
        }


class NoteCreateForm(ModelForm):
    class Meta:
        model = Note
        fields = ("text",)
        widgets = {
            "text": Textarea(
                attrs={
                    "rows": 3,
                    "class": "note_text note_typewatch",
                    "placeholder": gettext("Note of the day"),
                }
            )
        }

    def __init__(self, codex=None, *args, **kwargs):
        super(NoteCreateForm, self).__init__(*args, **kwargs)
        # The codex is needed to save the form
        if codex is not None:
            self.codex = codex

    def save(self, commit=True, *args, **kwargs):
        # Create a note object with the save method of ModelForm
        note = super(NoteCreateForm, self).save(commit=False)

        # Get the page of the day if it exist
        # TODO: try to upgrade the way this check is down ?
        today = get_current_timestamp().date()
        page = (
            Page.objects.filter(codex=self.codex, date=today)
                .select_related("note")
                .first()
        )
        # If the page does not exist, create a new one
        if page is None:
            page = Page(codex=self.codex, date=today)
            if commit:
                page.save()
        # Set the page of the note
        note.page = page

        if commit:
            note.save()
        return note


class NoteUpdateForm(AbstractHashFrom):
    class Meta:
        model = Note
        fields = ("text",)
        hash_field = "text"
        widgets = {
            "text": Textarea(
                attrs={
                    "rows": 3,
                    "class": "note_text note_typewatch",
                    "placeholder": gettext("Note of the day"),
                    "readonly": "",
                }
            )
        }


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("text", "is_achieved")
        widgets = {
            "text": Textarea(
                attrs={
                    "rows": 1,
                    "class": "task_text",
                    "placeholder": gettext("New task"),
                }
            ),
            "is_achieved": CheckboxInput(attrs={"class": "task_is_achieved"}),
        }

    def __init__(self, codex=None, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        # The codex is needed to save the form
        if codex is not None:
            self.codex = codex

    def save(self, commit=True, *args, **kwargs):
        # Create a task object with the save method of ModelForm
        task = super(TaskCreateForm, self).save(commit=False)

        # Get the page of the day if it exist
        # TODO: try to upgrade the way this check is down ?
        today = get_current_timestamp().date()
        page = (
            Page.objects.filter(codex=self.codex, date=today)
                .select_related("note")
                .first()
        )
        # If the page does not exist, create a new one
        if page is None:
            page = Page(codex=self.codex, date=today)
            if commit:
                page.save()
        # Add set the page of the note
        task.page = page

        if commit:
            task.save()
        return task


class TaskUpdateForm(AbstractHashFrom):
    class Meta:
        model = Task
        hash_field = "text"
        fields = ("text", "is_achieved")
        widgets = {
            "text": Textarea(
                attrs={
                    "rows": 1,
                    "class": "task_text",
                    "placeholder": gettext("New task"),
                }
            ),
            "is_achieved": CheckboxInput(attrs={"class": "task_is_achieved"}),
        }
