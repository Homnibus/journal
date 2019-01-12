from django.forms import ModelForm, Textarea, HiddenInput, CheckboxInput, IntegerField

from .models import Codex, Information, Note, Task


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
        codex = super(CodexForm, self).save(commit=False, *args, **kwargs)
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
            information = super(InformationForm, self).save(
                commit=False, *args, **kwargs
            )
        return information


class NoteForm(ModelForm):
    note_id = IntegerField(
        widget=HiddenInput(attrs={"class": "note_id"}), required=False
    )

    class Meta:
        model = Note
        fields = ("text",)
        widgets = {
            "text": Textarea(
                attrs={
                    "rows": 3,
                    "class": "note_text note_typewatch",
                    "placeholder": "Notes du jour",
                    "readonly": "",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        # If an object is given as a parameter, the id field must be updated
        if self.instance:
            self.initial["note_id"] = self.instance.id

    def save(self, commit=True, page=None, *args, **kwargs):
        """ Override the save method to manage the update case """
        # When updating
        if self.cleaned_data["note_id"] is not None:
            # Raise the exception if the Note does not exist
            note = Note.objects.get(id=self.cleaned_data["note_id"])
            note.text = self.cleaned_data["text"]
        # When creating
        else:
            note = super(NoteForm, self).save(commit=False, *args, **kwargs)
            # The page must be given otherwise the note can't be create
            note.page = page
        if commit:
            note.save()
        return note


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
            task = super(TaskForm, self).save(commit=False, *args, **kwargs)
            # The page must be given otherwise the note can't be create
            task.page = page
        if commit:
            task.save()
        return task
