from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    Textarea,
    HiddenInput,
    CheckboxInput,
    IntegerField,
    SlugField,
)
from django.utils.translation import gettext

from projets.commun.utils import java_string_hashcode
from .models import Codex, Information, Note, Task, get_current_timestamp, Page


class AbstractHashFrom(ModelForm):
    hash = IntegerField(
        label="hash", required=True, widget=HiddenInput(attrs={"class": "hash"})
    )
    id = IntegerField(
        label="id", required=True, widget=HiddenInput(attrs={"class": "id"})
    )

    def __init__(self, data=None, instance=None, *args, **kwargs):
        super(AbstractHashFrom, self).__init__(
            data=data, instance=instance, *args, **kwargs
        )
        # If an object is given as a parameter, update the hash field
        if instance:
            self.initial["hash"] = java_string_hashcode(
                self.initial[self.Meta.hash_field]
            )
            self.initial["id"] = self.instance.id

    def clean_id(self):
        model_id = self.cleaned_data["id"]
        # Check if the Model object exist in the database. Raise a Model.DoesNotExist if not
        if not self.Meta.model.objects.filter(id=model_id).exists():
            raise ValidationError(
                gettext(
                    "The server can't find the requested resource ({resource_name})."
                ).format(resource_name=self.Meta.model._meta.object_name)
            )
        return model_id

    def clean(self):
        cleaned_data = super(AbstractHashFrom, self).clean()

        model_id = cleaned_data.get("id")
        text_hash = cleaned_data.get("hash")
        # If there is not error on id and hash, check if the hash is the same as in the database
        if model_id is not None and text_hash is not None:
            model = self.Meta.model.objects.get(id=model_id)
            text = getattr(model, self.Meta.hash_field)
            if java_string_hashcode(text) != text_hash:
                raise ValidationError(
                    gettext(
                        "The ({resource_name}) have been modified since the last modification attempt."
                    ).format(resource_name=self.Meta.model._meta.object_name)
                )

        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        super(AbstractHashFrom, self).save(commit=False)

        # Get the model from the ID and set it as the form instance if not already done
        if self.instance.id is None:
            self.instance = self.Meta.model.objects.get(id=self.cleaned_data.get("id"))
            # Update the field given by the form to the model
            for field in [x for x in self.fields if x not in ["id", "hash"]]:
                setattr(self.instance, field, self.cleaned_data.get(field))

        # Save the model
        if commit:
            self.instance.save()

        return self.instance


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


class InformationForm(ModelForm):
    class Meta:
        model = Information
        fields = ("text",)
        widgets = {
            "text": Textarea(
                attrs={"rows": 3, "style": "resize:none;", "class": "information_text"}
            )
        }

    def save(self, commit=True, codex=None, *args, **kwargs):
        """ Override the save method to manage the update case """
        if commit:
            information = Information.objects.update_or_create(
                codex=codex,
                defaults={"codex": codex, "text": self.cleaned_data["text"]},
            )
        else:
            information = super(InformationForm, self).save(commit=False)
        return information


class NoteCreateFromSlugForm(ModelForm):
    codex_slug = SlugField(
        widget=HiddenInput(attrs={"class": "codex_slug"}), required=True
    )

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

    def clean_codex_slug(self):
        # Check if the given slug correspond to a codex present in the database
        codex_slug = self.cleaned_data["codex_slug"]
        if not Codex.objects.filter(slug=codex_slug).exists():
            raise ValidationError(
                gettext(
                    "The server can't find the requested resource ({resource_name})."
                ).format(resource_name=Codex._meta.object_name)
            )
        return codex_slug

    def clean(self):
        # Check if a Note already exist for the current day for the given codex
        cleaned_data = super(NoteCreateFromSlugForm, self).clean()
        codex_slug = cleaned_data.get("codex_slug")
        if codex_slug is not None:
            # Get the codex
            codex = Codex.objects.get(slug=codex_slug)
            # Get the page of the day
            # TODO: try to upgrade the way this check is down
            today = get_current_timestamp().date()
            page = (
                Page.objects.filter(codex=codex, date=today)
                    .select_related("note")
                    .first()
            )
            # If a note was already created for the page of the day, add an error
            if hasattr(page, "note"):
                raise ValidationError(
                    gettext("A Note already exist for today for this Codex.")
                )
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        """ Override the save method to manage the update case """
        # Create a note object with the save method of ModelForm
        note = super(NoteCreateFromSlugForm, self).save(commit=False)
        # Get the codex from the slug
        # TODO : Create a function out of this ?
        codex_slug = self.cleaned_data.get("codex_slug")
        codex = Codex.objects.get(slug=codex_slug)

        # Get the page of the day if it exist
        # TODO: try to upgrade the way this check is down ?
        today = get_current_timestamp().date()
        page = (
            Page.objects.filter(codex=codex, date=today).select_related("note").first()
        )
        # If the page does not exist, create a new one
        if page is None:
            page = Page(codex=codex, date=today)
            if commit:
                page.save()
        # Add set the page of the note
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


class TaskForm(ModelForm):
    task_id = IntegerField(
        widget=HiddenInput(attrs={"class": "task_id"}), required=False
    )

    class Meta:
        model = Task
        fields = ("text", "is_achieved")
        widgets = {
            "text": Textarea(
                attrs={"rows": 1, "class": "task_text", "placeholder": "Nouvelle tache"}
            ),
            "is_achieved": CheckboxInput(attrs={"class": "task_is_achieved"}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # If an object is given as a parameter, the id field must be updated
        if self.instance:
            self.initial["task_id"] = self.instance.id

    def save(self, commit=True, page=None, *args, **kwargs):
        """ Override the save method to manage the update case """
        # When updating
        if self.cleaned_data["task_id"] is not None:
            # Raise the exception if the task does not exist
            task = Task.objects.get(id=self.cleaned_data["task_id"])
            task.text = self.cleaned_data["text"]
            task.is_achieved = self.cleaned_data["is_achieved"]
        # When creating
        else:
            task = super(TaskForm, self).save(commit=False)
            # The page must be given otherwise the note can't be create
            task.page = page
        if commit:
            task.save()
        return task
