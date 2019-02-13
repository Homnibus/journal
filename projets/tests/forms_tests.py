from django.contrib.auth.models import User
from django.test import TestCase

from projets.commun.utils import java_string_hashcode
from projets.forms import (
    CodexForm,
    InformationUpdateForm,
    NoteUpdateForm,
    NoteCreateForm,
    TaskUpdateForm,
    TaskCreateForm,
    InformationCreateForm,
    TaskDeleteForm, NoteDeleteForm, InformationDeleteForm)
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


class InformationCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.input_data = {"text": self.text}

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = InformationCreateForm()
        self.assertIsNotNone(form.fields["text"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model. """
        form = InformationCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()
        form.save(commit=False)
        informations = Information.objects.all()

        self.assertEqual(len(informations), 0)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model. """
        form = InformationCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()
        form.save(commit=True)
        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)
        self.assertEqual(informations[0].text, self.text)
        self.assertEqual(informations[0].codex, self.codex)

    def test_save_text_empty_assert_text_validation_error(self):
        """ Test if the save method raise a validation error if a note already exist for that day. """
        self.input_data["text"] = ""
        form = InformationCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()

        self.assertIsNotNone(form.errors["text"])


class InformationUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.update_text = "Test Text 2"
        self.hash = java_string_hashcode(self.text)
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        self.input_data = {"text": self.update_text, "hash": self.hash}

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = InformationUpdateForm(instance=self.information)
        self.assertEqual(form.initial["text"], self.text)
        self.assertEqual(form.initial["hash"], self.hash)
        self.assertEqual(form.initial["id"], self.information.id)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model. """
        form = InformationUpdateForm(data=self.input_data, instance=self.information)
        form.is_valid()
        form.save()
        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)
        self.assertEqual(informations[0].text, self.update_text)

    def test_save_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the is_valid method add a hash form error id the given hash does not correspond to the database
        text hash.
        """
        input_data = self.input_data
        input_data["hash"] = 0
        form = InformationUpdateForm(data=input_data, instance=self.information)
        form.is_valid()
        self.assertIsNotNone(form.errors["hash"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model. """
        form = InformationUpdateForm(data=self.input_data, instance=self.information)
        form.is_valid()
        form.save(commit=False)
        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model. """
        form = InformationUpdateForm(data=self.input_data, instance=self.information)
        form.is_valid()
        form.save(commit=False)
        informations = Information.objects.all()

        self.assertEqual(informations[0].text, self.text)

    def test_save_assert_other_model_not_updated(self):
        """ Test if the save method with commit = true does not update other model. """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        Information.objects.create(codex=codex, text=self.text)
        form = InformationUpdateForm(data=self.input_data, instance=self.information)
        form.is_valid()
        form.save(commit=True)
        informations = Information.objects.all().order_by("id")

        self.assertEqual(len(informations), 2)
        self.assertEqual(informations[1].text, self.text)
        self.assertEqual(informations[1].codex, codex)


class InformationDeleteFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.hash = java_string_hashcode(self.text)
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        self.input_data = {"hash": self.hash}

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = InformationDeleteForm(instance=self.information)
        self.assertEqual(form.initial["hash"], self.hash)
        self.assertEqual(form.initial["id"], self.information.id)

    def test_delete_information_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the is_valid method add a hash form error if the given hash does not correspond to the database
        text hash.
        """
        self.input_data["hash"] = 0
        form = InformationDeleteForm(data=self.input_data, instance=self.information)
        form.is_valid()
        self.assertIsNotNone(form.errors["hash"])


class NoteCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.input_data = {"text": self.text}

    def test_creation_assert_fields_exist(self):
        """ Test if the form has the right fields. """
        form = NoteCreateForm()
        self.assertIsNotNone(form.fields["text"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model. """
        form = NoteCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()
        form.save(commit=False)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 0)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model. """
        form = NoteCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()
        form.save(commit=True)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, self.text)

    def test_save_text_empty_assert_text_validation_error(self):
        """ Test if the save method raise a validation error if the input text is empty. """
        self.input_data["text"] = ""
        form = NoteCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()

        self.assertIsNotNone(form.errors["text"])


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
        self.input_data = {"text": self.update_text, "hash": self.hash}

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = NoteUpdateForm(instance=self.note)
        self.assertEqual(form.initial["text"], self.text)
        self.assertEqual(form.initial["hash"], self.hash)
        self.assertEqual(form.initial["id"], self.note.id)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model. """
        form = NoteUpdateForm(data=self.input_data, instance=self.note)
        form.is_valid()
        form.save()
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, self.update_text)

    def test_save_note_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the is_valid method add a hash form error if the given hash does not correspond to the database
        text hash.
        """
        input_data = self.input_data
        input_data["hash"] = 0
        form = NoteUpdateForm(data=input_data, instance=self.note)
        form.is_valid()
        self.assertIsNotNone(form.errors["hash"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model. """
        form = NoteUpdateForm(data=self.input_data, instance=self.note)
        form.is_valid()
        form.save(commit=False)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model. """
        form = NoteUpdateForm(data=self.input_data, instance=self.note)
        form.is_valid()
        form.save(commit=False)
        notes = Note.objects.all()

        self.assertEqual(notes[0].text, self.text)

    def test_save_assert_other_model_not_updated(self):
        """ Test if the save method with commit = true does not update other model. """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        Note.objects.create(page=page, text=self.text)
        form = NoteUpdateForm(data=self.input_data, instance=self.note)
        form.is_valid()
        form.save(commit=True)
        notes = Note.objects.all().order_by("id")

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[1].text, self.text)
        self.assertEqual(notes[1].page, page)


class NoteDeleteFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.text = "Test Text"
        self.hash = java_string_hashcode(self.text)
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.input_data = {
            "hash": self.hash,
        }

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = NoteDeleteForm(instance=self.note)
        self.assertEqual(form.initial["hash"], self.hash)
        self.assertEqual(form.initial["id"], self.note.id)

    def test_delete_note_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the is_valid method add a hash form error if the given hash does not correspond to the database
        text hash.
        """
        self.input_data["hash"] = 0
        form = NoteDeleteForm(data=self.input_data, instance=self.note)
        form.is_valid()
        self.assertIsNotNone(form.errors["hash"])


class TaskCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.is_achieved = False
        self.input_data = {"text": self.text, "is_achieved": self.is_achieved}

    def test_creation_assert_needed_param_exist(self):
        """ Test if the form has the right fields. """
        form = TaskCreateForm()
        self.assertIsNotNone(form.fields["text"])
        self.assertIsNotNone(form.fields["is_achieved"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model. """
        form = TaskCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()
        form.save(commit=False)
        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 0)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model. """
        form = TaskCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()
        form.save(commit=True)
        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, self.text)
        self.assertEqual(tasks[0].is_achieved, self.is_achieved)

    def test_save_text_empty_assert_text_validation_error(self):
        """ Test if the save method raise a validation error if the input text is empty. """
        self.input_data["text"] = ""
        form = TaskCreateForm(data=self.input_data, codex=self.codex)
        form.is_valid()

        self.assertIsNotNone(form.errors["text"])


class TaskUpdateFormTest(TestCase):
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
        self.update_is_achieved = True
        self.update_text = "Test Text 2"
        self.hash = java_string_hashcode(self.text)
        self.task = Task.objects.create(page=self.page, text=self.text)
        self.input_data = {
            "text": self.update_text,
            "hash": self.hash,
            "is_achieved": self.update_is_achieved,
        }

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = TaskUpdateForm(instance=self.task)
        self.assertEqual(form.initial["text"], self.text)
        self.assertEqual(form.initial["is_achieved"], self.is_achieved)
        self.assertEqual(form.initial["hash"], self.hash)
        self.assertEqual(form.initial["id"], self.task.id)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model. """
        form = TaskUpdateForm(data=self.input_data, instance=self.task)
        form.is_valid()
        form.save()
        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, self.update_text)
        self.assertEqual(tasks[0].is_achieved, self.update_is_achieved)

    def test_save_task_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the is_valid method add a hash form error if the given hash does not correspond to the database
        text hash.
        """
        self.input_data["hash"] = 0
        form = TaskUpdateForm(data=self.input_data, instance=self.task)
        form.is_valid()
        self.assertIsNotNone(form.errors["hash"])

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model. """
        form = TaskUpdateForm(data=self.input_data, instance=self.task)
        form.is_valid()
        form.save(commit=False)
        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model. """
        form = TaskUpdateForm(data=self.input_data, instance=self.task)
        form.is_valid()
        form.save(commit=False)
        tasks = Task.objects.all()

        self.assertEqual(tasks[0].text, self.text)

    def test_save_assert_other_model_not_updated(self):
        """ Test if the save method with commit = true does not update other model """
        Task.objects.create(
            page=self.page, text=self.text, is_achieved=self.is_achieved
        )
        form = TaskUpdateForm(data=self.input_data, instance=self.task)
        form.is_valid()
        form.save(commit=True)
        tasks = Task.objects.all().order_by("id")

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1].text, self.text)
        self.assertEqual(tasks[1].is_achieved, self.is_achieved)


class TaskDeleteFormTest(TestCase):
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
        self.hash = java_string_hashcode(self.text)
        self.task = Task.objects.create(page=self.page, text=self.text)
        self.input_data = {
            "hash": self.hash,
        }

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form. """
        form = TaskDeleteForm(instance=self.task)
        self.assertEqual(form.initial["hash"], self.hash)
        self.assertEqual(form.initial["id"], self.task.id)

    def test_delete_task_hash_not_same_as_bdd_assert_form_validation_error(self):
        """
        Test if the is_valid method add a hash form error if the given hash does not correspond to the database
        text hash.
        """
        self.input_data["hash"] = 0
        form = TaskDeleteForm(data=self.input_data, instance=self.task)
        form.is_valid()
        self.assertIsNotNone(form.errors["hash"])
