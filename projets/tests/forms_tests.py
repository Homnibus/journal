from django.contrib.auth.models import User
from django.test import TestCase

from projets.commun.utils import java_string_hashcode
from projets.forms import (
    CodexForm,
    InformationForm,
    TaskForm,
    NoteUpdateForm,
    NoteCreateFromSlugForm,
)
from projets.models import Codex, Information, Page, Note, Task


class CodexFormTest(TestCase):
    def setUp(self):
        self.title = "Test Codex 1"
        self.description = "Description 1"
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title=self.title, author=self.user, description=self.description
        )
        self.form = CodexForm(instance=self.codex)

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form """
        self.assertEqual(self.form.initial["title"], self.title)
        self.assertEqual(self.form.initial["description"], self.description)

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model """
        title = "Test Codex 2"
        description = "Description 2"
        input_data = {"title": title, "description": description}
        form = CodexForm(input_data)
        form.is_valid()
        form.save(commit=False, author=self.user)
        codexs = Codex.objects.all()

        self.assertEqual(len(codexs), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other the model """
        title = "Test Codex 2"
        description = "Description 2"
        input_data = {"title": title, "description": description}
        form = CodexForm(input_data)
        form.is_valid()
        form.save(commit=False, author=self.user)
        codexs = Codex.objects.all()

        self.assertEqual(codexs[0].title, self.title)
        self.assertEqual(codexs[0].description, self.description)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model """
        title = "Test Codex 2"
        description = "Description 2"
        input_data = {"title": title, "description": description}
        form = CodexForm(input_data)
        form.is_valid()
        form.save(commit=True, author=self.user)
        codexs = Codex.objects.filter(title=title)

        self.assertEqual(len(codexs), 1)
        self.assertEqual(codexs[0].title, title)
        self.assertEqual(codexs[0].description, description)

    def test_save_commit_true_assert_not_updated(self):
        """ Test if the save method with commit = true does not update other model """
        title = "Test Codex 2"
        description = "Description 2"
        input_data = {"title": title, "description": description}
        form = CodexForm(input_data)
        form.is_valid()
        form.save(commit=True, author=self.user)
        codexs = Codex.objects.all().order_by("id")

        self.assertEqual(len(codexs), 2)
        self.assertEqual(codexs[0].title, self.title)
        self.assertEqual(codexs[0].description, self.description)


class InformationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        self.form = InformationForm(instance=self.information)

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form """
        self.assertEqual(self.form.initial["text"], self.text)

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model """
        text = "Test Text 2"
        input_data = {"text": text}
        form = InformationForm(input_data)
        form.is_valid()
        form.save(commit=False, codex=self.codex)
        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model """
        text = "Test Text 2"
        input_data = {"text": text}
        form = InformationForm(input_data)
        form.is_valid()
        form.save(commit=False, codex=self.codex)
        informations = Information.objects.all()

        self.assertEqual(informations[0].text, self.text)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        text = "Test Text 2"
        input_data = {"text": text}
        form = InformationForm(input_data)
        form.is_valid()
        form.save(commit=True, codex=codex)
        informartions = Information.objects.filter(text=text)

        self.assertEqual(len(informartions), 1)
        self.assertEqual(informartions[0].text, text)
        self.assertEqual(informartions[0].codex, codex)

    def test_save_commit_true_assert_model_not_updated(self):
        """ Test if the save method with commit = true does update other model """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        text = "Test Text 2"
        input_data = {"text": text}
        form = InformationForm(input_data)
        form.is_valid()
        form.save(commit=True, codex=codex)
        informartions = Information.objects.all().order_by("id")

        self.assertEqual(len(informartions), 2)
        self.assertEqual(informartions[0].text, self.text)
        self.assertEqual(informartions[0].codex, self.codex)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model """
        text = "Test Text 2"
        input_data = {"text": text}
        form = InformationForm(input_data)
        form.is_valid()
        form.save(codex=self.codex)
        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)
        self.assertEqual(informations[0].text, text)


class NoteCreateFromSlugFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.input_data = {"text": self.text, "codex_slug": self.codex.slug}

    def test_creation_assert_fields_exist(self):
        """ Test if the form has the right fields """
        form = NoteCreateFromSlugForm()
        self.assertIsNotNone(form.fields["text"])
        self.assertIsNotNone(form.fields["codex_slug"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model """
        form = NoteCreateFromSlugForm(self.input_data)
        form.is_valid()
        form.save(commit=False)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 0)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model """
        form = NoteCreateFromSlugForm(self.input_data)
        form.is_valid()
        form.save(commit=True)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, self.text)

    def test_save_codex_not_exist_assert_slug_validation_error(self):
        """ Test if the save method raise a validation error if the codex does not exist """
        input_data = self.input_data.copy()
        input_data["codex_slug"] = "error-codex-slug"
        form = NoteCreateFromSlugForm(input_data)
        form.is_valid()
        self.assertIsNotNone(form.errors["codex_slug"])

    def test_save_commit_true_note_exist_assert_global_validation_error(self):
        """ Test if the save method raise a validation error if a note already exist for that day """
        page = Page.objects.create(codex=self.codex)
        Note.objects.create(page=page, text="Test Text")
        form = NoteCreateFromSlugForm(self.input_data)
        form.is_valid()

        self.assertIsNotNone(form.errors["__all__"])


class NoteUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.text = "Test Text"
        self.update_text = "Test Text 2"
        self.hash = java_string_hashcode(self.text)
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.input_data = {"text": self.update_text, "hash": self.hash, "id": 1}

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form """
        form = NoteUpdateForm(instance=self.note)
        self.assertEqual(form.initial["text"], self.text)
        self.assertEqual(form.initial["id"], self.note.id)
        self.assertEqual(form.initial["hash"], self.hash)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model """
        form = NoteUpdateForm(self.input_data)
        form.is_valid()
        form.save()
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, self.update_text)

    def test_save_note_does_not_exist_assert_id_validation_error(self):
        """
        Test if the is_valid method add a form error on the id field if the given id does not refer to a data base
        object
        """
        input_data = self.input_data
        input_data["id"] = 0
        form = NoteUpdateForm(self.input_data)
        form.is_valid()
        self.assertIsNotNone(form.errors["id"])

    def test_save_note_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the si_valid method add a global form error id the given hash does not correspond to the database
        text hash
        """
        input_data = self.input_data
        input_data["hash"] = 0
        form = NoteUpdateForm(self.input_data)
        form.is_valid()
        self.assertIsNotNone(form.errors["__all__"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model """
        form = NoteUpdateForm(self.input_data)
        form.is_valid()
        form.save(commit=False)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model """
        form = NoteUpdateForm(self.input_data)
        form.is_valid()
        form.save(commit=False)
        notes = Note.objects.all()

        self.assertEqual(notes[0].text, self.text)

    def test_save_commit_true_assert_model_not_updated(self):
        """ Test if the save method with commit = true does not update other model """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        note = Note.objects.create(page=page, text=self.text)
        input_data = self.input_data
        input_data["id"] = note.id
        form = NoteUpdateForm(input_data)
        form.is_valid()
        form.save(commit=True)
        notes = Note.objects.all().order_by("id")

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, self.text)
        self.assertEqual(notes[0].page, self.page)


class TaskFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.text = "Test Text"
        self.is_achieved = False
        self.task = Task.objects.create(page=self.page, text=self.text)
        self.form = TaskForm(instance=self.task)

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form """
        self.assertEqual(self.form.initial["text"], self.text)
        self.assertEqual(self.form.initial["is_achieved"], self.is_achieved)
        self.assertEqual(self.form.initial["task_id"], self.task.id)

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model """
        text = "Test Text 2"
        input_data = {"text": text, "is_achieved": self.task.is_achieved}
        form = TaskForm(input_data)
        form.is_valid()
        form.save(commit=False, page=self.page)
        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model """
        text = "Test Text 2"
        input_data = {"text": text, "is_achieved": self.task.is_achieved}
        form = TaskForm(input_data)
        form.is_valid()
        form.save(commit=False, page=self.page)
        tasks = Task.objects.all()

        self.assertEqual(tasks[0].text, self.text)

    def test_save_commit_assert_new_model_created(self):
        """ Test if the save method with commit = true does create the model """
        text = "Test Text 2"
        is_achieved = True
        input_data = {"text": text, "is_achieved": is_achieved}
        form = TaskForm(input_data)
        form.is_valid()
        form.save(commit=True, page=self.page)
        tasks = Task.objects.filter(text=text)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, text)
        self.assertEqual(tasks[0].is_achieved, is_achieved)

    def test_save_commit_assert_new_model_not_updated(self):
        """ Test if the save method with commit = true does not update other model """
        text = "Test Text 2"
        is_achieved = True
        input_data = {"text": text, "is_achieved": is_achieved}
        form = TaskForm(input_data)
        form.is_valid()
        form.save(commit=True, page=self.page)
        tasks = Task.objects.all().order_by("id")

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].text, self.text)
        self.assertEqual(tasks[0].is_achieved, self.is_achieved)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model """
        text = "Test Text 2"
        is_achieved = True
        input_data = {"text": text, "task_id": self.task.id, "is_achieved": is_achieved}
        form = TaskForm(input_data)
        form.is_valid()
        form.save()
        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, text)
        self.assertEqual(tasks[0].is_achieved, is_achieved)
