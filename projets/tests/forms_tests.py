from django.contrib.auth.models import User
from django.test import TestCase

from projets.forms import CodexForm, InformationForm, NoteForm, TaskForm
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


class NoteFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.text = "Test Text"
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.form = NoteForm(instance=self.note)

    def test_creation_assert_needed_param_exist(self):
        """ Test if the required parameters are added after the creation of the form """
        self.assertEqual(self.form.initial["text"], self.text)
        self.assertEqual(self.form.initial["note_id"], self.note.id)

    def test_save_commit_false_assert_model_not_created(self):
        """ Test if the save method with commit = false does not create the model """
        text = "Test Text 2"
        input_data = {"text": text}
        form = NoteForm(input_data)
        form.is_valid()
        form.save(commit=False, page=self.page)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)

    def test_save_commit_false_assert_model_not_updated(self):
        """ Test if the save method with commit = false does not update other model """
        text = "Test Text 2"
        input_data = {"text": text}
        form = NoteForm(input_data)
        form.is_valid()
        form.save(commit=False, page=self.page)
        notes = Note.objects.all()

        self.assertEqual(notes[0].text, self.text)

    def test_save_commit_true_assert_model_created(self):
        """ Test if the save method with commit = true does create the model """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        text = "Test Text 2"
        input_data = {"text": text}
        form = NoteForm(input_data)
        form.is_valid()
        form.save(commit=True, page=page)
        notes = Note.objects.filter(text=text)

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, text)
        self.assertEqual(notes[0].page, page)

    def test_save_commit_true_assert_model_not_updated(self):
        """ Test if the save method with commit = true does not update other model """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        text = "Test Text 2"
        input_data = {"text": text}
        form = NoteForm(input_data)
        form.is_valid()
        form.save(commit=True, page=page)
        notes = Note.objects.all().order_by("id")

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, self.text)
        self.assertEqual(notes[0].page, self.page)

    def test_save_assert_model_updated(self):
        """ Test if the save method update the model """
        text = "Test Text 2"
        input_data = {"text": text, "note_id": self.note.id}
        form = NoteForm(input_data)
        form.is_valid()
        form.save()
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, text)


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
